from ..config import get_config,Config
from ..dao.type_ import DependencyContext

class MainController:
    def __init__(self):
        self.config = get_config()

    def start_dependency(self)->DependencyContext:
        ...

    def start_ui(self,dependency_context:DependencyContext):
        ...
    
    def start_backup(self,dependency_context:DependencyContext):
        sacn_service = ScanService(DependencyContext)
        deduplication_service = DeduplicationService(DependencyContext)
        compress_service = CompressService(DependencyContext)
        verification_service = VerificationService(DependencyContext)
        backup_service = BackupService(DependencyContext)
        


    def run(self):
        dependency_context = self.start_dependency()
        self.start_ui(dependency_context)
        self.start_backup(dependency_context)




if __name__ == "__main__":
    main = MainController([1])
    main.run()