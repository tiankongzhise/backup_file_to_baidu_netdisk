from typing import Literal
from sqlalchemy import BigInteger, String,Integer,JSON,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass,Mapped,mapped_column
from time import time

class BaseModel(MappedAsDataclass, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,init=False)
    created_at: Mapped[int] = mapped_column(BigInteger, default=int(time()), init=False)
    updated_at: Mapped[int] = mapped_column(BigInteger, onupdate=int(time()),nullable=True, init=False)
    latest_at: Mapped[int] = mapped_column(BigInteger, default=int(time()), onupdate=int(time()),init=False)

class ObjectMetaData(BaseModel):
    __tablename__ = "object_meta_data"
    object_id: Mapped[int] = mapped_column(String(255),comment="对象唯一标识，路径hash256+设备ID")
    object_name: Mapped[str] = mapped_column(String(255),comment="对象名称，文件名或文件夹名")
    local_path: Mapped[str] = mapped_column(String(255),comment="本地路径，完整路径")
    object_size: Mapped[int] = mapped_column(BigInteger,comment="对象大小，字节")
    md5_hash: Mapped[str] = mapped_column(String(32),comment="MD5哈希，32位",nullable=True)
    sha1_hash: Mapped[str] = mapped_column(String(40),comment="SHA1哈希，40位",nullable=True)
    process_stage: Mapped[int] = mapped_column(Integer,comment="处理阶段")
    process_status: Mapped[int] = mapped_column(Integer,comment="处理状态")
    backup_status: Mapped[int] = mapped_column(Integer,comment="备份状态，0:未开始，1:备份中，2:备份成功，3:备份失败，4:备份取消，5:备份异常",nullable=True)
    remote_path: Mapped[str] = mapped_column(String(255),comment="远程路径，百度云盘路径",nullable=True)
    remote_etag: Mapped[str] = mapped_column(String(255),comment="百度云盘备份成功返回的md5,用于一致性检查",nullable=True)
    encrypted_remote_name_path: Mapped[str] = mapped_column(String(255),comment="文件名加密后的远程路径，百度云盘路径",nullable=True)
    encrypted_remote_etag: Mapped[str] = mapped_column(String(255),comment="文件名加密后的远程etag，百度云盘备份成功返回的md5,用于一致性检查",nullable=True)
    __table_args__ = (UniqueConstraint('object_id', name='uix_object_id'),)

class ObjectDetails(BaseModel):
    __tablename__ = "object_details"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    object_name: Mapped[str] = mapped_column(String(255),comment="对象名称，文件名或文件夹名")
    local_path: Mapped[str] = mapped_column(String(255),comment="本地路径，完整路径")
    object_size: Mapped[int] = mapped_column(BigInteger,comment="对象大小，字节")
    object_count: Mapped[dict] = mapped_column(JSON,comment="对象数量，文件夹数量,总对象数量")
    details: Mapped[dict] = mapped_column(JSON,comment="对象详情,包括文件名、文件类型、路径、大小、修改时间、创建时间、访问时间、权限等，数据结构为list[dict]")


class ProcessTask(BaseModel):
    __tablename__ = "process_task"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    process_stage:Mapped[int] = mapped_column(Integer,comment="处理阶段")
    process_status:Mapped[int] = mapped_column(Integer,comment="处理状态")
    error_message:Mapped[str] = mapped_column(String(255),comment="错误信息",nullable=True)
    __table_args__ = (UniqueConstraint('object_id_process_stage', name='uix_object_id_process_stage'),)

class TransferTask(BaseModel):
    __tablename__ = "transfer_tasks"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    task_type:Mapped[Literal['upload','download']] = mapped_column(String(10),comment="任务类型")
    total_chunks:Mapped[int] = mapped_column(Integer,comment="总分块数")
    completed_chunks:Mapped[int] = mapped_column(Integer,comment="已完成分块数")
    chunk_size:Mapped[int] = mapped_column(Integer,comment="分块大小，字节")
    chunk_upload_ids:Mapped[dict] = mapped_column(JSON,comment="分块上传ID列表")
    status:Mapped[Literal['未开始','备份中','备份完成','备份失败','备份取消','备份异常']] = mapped_column(String(10),comment="任务状态")
    retry_count:Mapped[int] = mapped_column(Integer,comment="重试次数",default=0)
    error_message:Mapped[str] = mapped_column(String(255),comment="错误信息",nullable=True) # type: ignore

class ProcessStageMapping(BaseModel):
    __tablename__ = "process_stage_mapping"
    process_stage:Mapped[int] = mapped_column(Integer,comment="处理阶段")
    process_stage_name:Mapped[str] = mapped_column(String(255),comment="处理阶段名称")
    process_stage_description:Mapped[str] = mapped_column(String(255),comment="处理阶段描述")

class ProcessStatusMapping(BaseModel):
    __tablename__ = "process_status_mapping"
    process_status:Mapped[int] = mapped_column(Integer,comment="处理状态")
    process_status_name:Mapped[str] = mapped_column(String(255),comment="处理状态名称")
    process_status_description:Mapped[str] = mapped_column(String(255),comment="处理状态描述")

class ScanTasks(BaseModel):
    __tablename__ = "scan_task"
    device_id:Mapped[str] = mapped_column(String(255),comment="设备ID")
    root_sequence:Mapped[list[str]] = mapped_column(JSON,comment="根目录序列，用于校验根目录顺序")
    completed_root_sequence:Mapped[dict] = mapped_column(JSON,comment="已完成根目录序列")
    scan_root_path:Mapped[str] = mapped_column(String(255),comment="扫描文件路径")
    total_objects:Mapped[int] = mapped_column(Integer,comment="总对象数")
    completed_objects:Mapped[int] = mapped_column(Integer,comment="已完成对象数")
    task_sequence:Mapped[list[str]] = mapped_column(JSON,comment="需要扫描的文件列表")
    completed_sequence:Mapped[dict] = mapped_column(JSON,comment="已完成扫描的文件列表")
    __table_args__ = (UniqueConstraint('device_id', name='uix_device_id'),)

class CompressionTasks(BaseModel):
    __tablename__ = "compression_task"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    total_files:Mapped[int] = mapped_column(Integer,comment="总文件数")
    completed_files:Mapped[int] = mapped_column(Integer,comment="已完成文件数")
    completed_file_name:Mapped[list[str]] = mapped_column(String(255),comment="最新完成文件名列表")
    task_sequence:Mapped[list[str]] = mapped_column(JSON,comment="压缩文件序列，用于校验压缩顺序")
    __table_args__ = (UniqueConstraint('object_id', name='uix_object_id'),)

class VerificationTasks(BaseModel):
    __tablename__ = "verification_task"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    target_hash_hex:Mapped[str] = mapped_column(String(64),comment="目标hash值的hex字符串")
    total_files:Mapped[int] = mapped_column(Integer,comment="总文件数")
    completed_files:Mapped[int] = mapped_column(Integer,comment="已完成文件数")
    completed_file_name:Mapped[list[str]] = mapped_column(String(255),comment="最新完成文件名列表")
    task_sequence:Mapped[list[str]] = mapped_column(JSON,comment="压缩文件序列，用于校验压缩顺序")
    hex_string:Mapped[str] = mapped_column(String(255),comment="hex字符串，当前hash值的hex字符串")
    __table_args__ = (UniqueConstraint('object_id', name='uix_object_id'),)

class BackupTasks(BaseModel):
    __tablename__ = "backup_task"
    object_id: Mapped[int] = mapped_column(String(255),comment="关联object_meta_data的object_id")
    operation:Mapped[Literal['upload','download','delete']] = mapped_column(String(10),comment="操作类型")
    priority:Mapped[int] = mapped_column(Integer,comment="优先级,1-10,1最高",default=1)
    retry_count:Mapped[int] = mapped_column(Integer,comment="重试次数",default=0)
    max_retries:Mapped[int] = mapped_column(Integer,comment="最大重试次数",default=3)
    __table_args__ = (UniqueConstraint('object_id', name='uix_object_id'),)

class ServiceStatusManager(BaseModel):
    __tablename__ = "service_status_manager"
    service_name:Mapped[str] = mapped_column(String(255),comment="服务名称")
    service_status:Mapped[Literal['未启动','启动中','运行中','运行结束','运行异常终止','运行异常']] = mapped_column(String(20),comment="服务状态")
    version:Mapped[int] = mapped_column(Integer,comment="版本号")
    __table_args__ = (UniqueConstraint('service_name','version', name='uix_service_name_version'),)