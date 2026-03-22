class BaiduPanClient:
    """百度网盘API客户端（封装认证与重试逻辑）"""
    
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = "https://d.pcs.baidu.com/rest/2.0/pcs"
    
    async def get_file_metadata(self, remote_path: str) -> dict:
        """获取云端文件元数据（含MD5/ETag）"""
        # GET /file?method=metadata&path={remote_path}
        pass
    
    async def precreate_superfile(self, remote_path: str, size: int, 
                                   block_list: list) -> dict:
        """预创建超级文件（分片上传准备）"""
        # POST /file?method=precreate
        # 返回 upload_id 用于后续分片上传[citation:5]
        pass
    
    async def upload_part(self, upload_id: str, part_seq: int, 
                          chunk_data: bytes) -> dict:
        """上传分片"""
        # POST /file?method=uploadpart&uploadid={upload_id}&partseq={part_seq}
        pass
    
    async def create_superfile(self, upload_id: str, block_list: list) -> dict:
        """合并分片完成上传"""
        # POST /file?method=createsuperfile
        pass
    
    async def download_with_range(self, remote_path: str, 
                                   start: int, end: int) -> bytes:
        """范围下载（支持断点续传）"""
        # GET /file?method=download&path={remote_path}
        # Headers: Range: bytes={start}-{end}
        pass

async def upload_with_resume(file_path: str, remote_path: str):
    """带断点续传的文件上传"""
    # 1. 检查是否有未完成的任务
    task = db.get_pending_task(file_path)
    
    if task and task.status == 'paused':
        # 2. 恢复上传：使用已保存的upload_id
        upload_id = task.chunk_upload_ids
        completed = task.completed_chunks
    else:
        # 3. 首次上传：分片并预创建
        chunks = split_file(file_path, chunk_size=10*1024*1024)  # 10MB分片
        result = await client.precreate_superfile(
            remote_path, file_size, [hash(c) for c in chunks]
        )
        upload_id = result['upload_id']
        db.create_task(file_path, upload_id, total_chunks=len(chunks))
        completed = 0
    
    # 4. 从断点继续上传
    for seq in range(completed, total_chunks):
        chunk = read_chunk(file_path, seq)
        await client.upload_part(upload_id, seq, chunk)
        db.update_progress(task.id, seq + 1)  # 每完成一分片立即持久化
    
    # 5. 合并分片
    await client.create_superfile(upload_id, block_list)
    db.mark_completed(task.id)