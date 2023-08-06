class Camera:
    def __init__(
        self,
        cid: str,
        dataservce,
        current_task: str = "",
        hardware_platform: str = "K2",
        address: str = "",
        system_state: str = "",
    ):
        self.id = cid
        self.dataservice = dataservce
        self.current_task = current_task
        self.hardware_platform = hardware_platform
        self.address = address
        self.system_state = system_state

    @classmethod
    def from_json(
        cls,
        dataservice,
        RowKey: str,
        currentTask: str = "",
        hardwarePlatform: str = "K2",
        address: str = "",
        systemState: str = "",
        *args,
        **kwargs
    ):
        return Camera(
            cid=RowKey,
            dataservce=dataservice,
            current_task=currentTask,
            hardware_platform=hardwarePlatform,
            address=address,
            system_state=systemState,
        )

    def set_stitching_status(self, status: str):
        self.dataservice.set_camera_stitching_status(self.id, status)
