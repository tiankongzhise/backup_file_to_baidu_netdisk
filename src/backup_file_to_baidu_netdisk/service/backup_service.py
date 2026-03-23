class SyncService:
    """同步引擎核心接口"""
    
    async def start_sync(self, sync_root: str):
        """启动同步（初始化监控+全量扫描）"""
        pass
    
    async def pause_sync(self):
        """暂停同步"""
        pass
    
    async def force_sync(self, file_path: str):
        """强制同步指定文件（用户手动触发）"""
        pass
    
    async def get_sync_status(self) -> SyncStatus:
        """获取同步状态（进度/队列/错误）"""
        pass

