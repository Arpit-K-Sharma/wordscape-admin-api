# app/service/order_service.py
import configparser
from typing import Any, Dict, List
import os
import boto3
from typing import Dict, List
from fastapi import UploadFile, HTTPException
from app.dto.order_dto import OrderDTO, OrderResponseDTO
from app.dto.project_tracking_dto import ProjectTrackingDTO
from app.repository.order_repository import OrderRepository
from app.dto.order_dto import OrderStatus
from app.config.logger_config import get_logger

logger = get_logger()
config = configparser.ConfigParser()
config.read('config.ini')

class OrderService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config['aws']['aws_access_key_id'],
            aws_secret_access_key=config['aws']['aws_secret_access_key'],
            region_name=config['aws']['aws_region_name']
        )
        self.repository = OrderRepository()
        self.bucket_name = config['aws']['aws_bucket_name']
        self.invoice_directory = config['aws']['aws_s3_invoice_path']
        self.order_directory = config['aws']['aws_s3_order_path']

    async def get_all_orders(self, page_number: int, page_size: int, sort_field: str, sort_direction: str) -> OrderResponseDTO:
        orders = await self.repository.find_all_orders(page_number, page_size, sort_field, sort_direction)
        total_elements = await self.repository.count_orders()
        
        # Fetch related data for each order
        enriched_orders = []
        for order in orders:
            enriched_order = await self.enrich_order_data(order)
            enriched_orders.append(enriched_order)

        return OrderResponseDTO(
            orders=[OrderDTO.from_order_collection(order) for order in enriched_orders],
            total_elements=total_elements
        )

    async def get_order_by_id(self, order_id: str) -> OrderDTO:
        order = await self.repository.find_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        enriched_order = await self.enrich_order_data(order)
        return OrderDTO.from_order_collection(enriched_order)

    async def enrich_order_data(self, order: Dict) -> Dict:
        # Fetch related data
        order['innerPaperType'] = await self.repository.get_paper_name(order['innerPaper'].id)
        order['outerPaperType'] = await self.repository.get_paper_name(order['outerPaper'].id)
        order['innerLamination'] = await self.repository.get_lamination_name(order['innerLamination'].id)
        order['outerLamination'] = await self.repository.get_lamination_name(order['outerLamination'].id)
        order['customer'] = await self.repository.get_customer_name(order['customer'].id)

        # Convert binding and inkType from comma-separated string to list
        order['bindingType'] = order.get('binding', '').split(',')
        order['inkType'] = order.get('inkType', '').split(',')

        return order


    async def enrich_order_data_for_job_card(self, order: Dict) -> Dict:
        # Fetch related data
        inner_paper = order.pop('innerPaper', None)
        outer_paper = order.pop('outerPaper', None)
        inner_lamination = order.pop('innerLamination', None)
        outer_lamination = order.pop('outerLamination', None)
        customer_id = order.pop('customer', None)

        if inner_paper:
            order['innerPaperType'] = await self.repository.get_paper_name(inner_paper.id)
        if outer_paper:
            order['outerPaperType'] = await self.repository.get_paper_name(outer_paper.id)
        if inner_lamination:
            order['innerLamination'] = await self.repository.get_lamination_name(inner_lamination.id)
        if outer_lamination:
            order['outerLamination'] = await self.repository.get_lamination_name(outer_lamination.id)
        if customer_id:
            order['customer'] = await self.repository.get_customer(customer_id.id)

        # Convert binding and inkType from comma-separated string to list
        binding = order.pop('binding', '')
        order['bindingType'] = binding.split(',') if binding else []
        
        ink_type = order.pop('inkType', '')
        order['inkType'] = ink_type.split(',') if ink_type else []

        # Initialize specified fields to None if they don't exist
        fields_to_initialize = [
            'job_card_id', 'prePressUnitList', 'deliveryDetail', 'prePressData',
            'paperDetailData', 'plateDetailData', 'paperData', 'pressUnitData',
            'costCalculation', 'binderyData'
        ]
        
        for field in fields_to_initialize:
            if field not in order:
                order[field] = None

        # Check if costCalculation exists and set billingInfo to None if it doesn't exist
        if 'costCalculation' in order and order['costCalculation'] is not None:
            if 'billingInfo' not in order['costCalculation']:
                order['costCalculation']['billingInfo'] = None
        else:
            # If costCalculation doesn't exist or is None, create it with billingInfo set to None
            order['costCalculation'] = {'billingInfo': None}

        return order


    
    async def cancel_order(self, order_id: str):
        result = await self.repository.cancel_order(order_id)
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Order could not be cancelled")
        return "Order Cancelled Successfully"
    
    
    ################# PROJECT TRACKING ##########################################

    async def get_project_tracking(self, order_id: str) -> ProjectTrackingDTO:
        order = await self.repository.find_order_by_id(order_id)
        if not order or not order.get('projectTracking'):
            return None
        
        project_tracking_data = order['projectTracking']
        return ProjectTrackingDTO(**project_tracking_data)


    async def update_project_tracking(self, order_id: str, tracking_data: Dict[str, bool]) -> ProjectTrackingDTO:
        updated_order = await self.repository.update_project_tracking(order_id, tracking_data)
        if updated_order:
            return "Project Tracking Updated"
        raise HTTPException(status_code=400,detail="Error Updating Project Tracking")

    #################### PDF DOWNLOAD ###################################################

    async def download_pdf(self, filename: str) -> bytes:
        logger.info(f"Downloading PDF for: {filename}")
        try:
            key = filename.replace('\\', '/')
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()
        except Exception as e:
            logger.error(f"Failed to download file from S3: {e}")
            raise RuntimeError(f"Failed to download file from S3: {str(e)}")
 
    async def get_invoice_by_id(self, id: str) -> bytes:
        order = await self.get_order_by_id(id)
        if not order:
            raise ValueError("Order not found")
        
        filename = f"{order.orderId}_{order.customer.replace(' ', '_')}"
        file_path = f"{self.invoice_directory}/{filename}.pdf"
        return await self.download_pdf(file_path)
    
    async def get_pdf_for_order(self, filename:str):
        file_path = os.path.join(self.order_directory, filename)
        return await self.download_pdf(file_path)
    
    async def get_order_pdf_filenames(self, order_id: str) -> list[str]:
        order = await self.repository.find_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        if not order['pdfFilename']:
            return []
        
        return order['pdfFilename']
