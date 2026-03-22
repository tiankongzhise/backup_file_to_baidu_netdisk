class DeduplicationService:
    """去重服务"""
    
    async def calculate_file_hash(self, file_path: str) -> FileHash:
        """计算文件哈希值（MD5+SHA1）"""
        pass
    
    async def check_duplicate_global(self, file_hash: FileHash) -> bool:
        """全局去重检查（跨设备）"""
        pass
    
    async def check_duplicate_local(self, file_hash: FileHash, 
                                      device_id: str) -> bool:
        """本地去重检查（单设备内）"""
        pass