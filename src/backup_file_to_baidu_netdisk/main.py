from .controller.service_manager import ServiceManager


def main():
    service_manager = ServiceManager()
    service_manager.start_service('all')

if __name__ == "__main__":
    main()