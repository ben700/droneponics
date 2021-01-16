from devicePayload import  getDeviceStatePayload
import connect

def droneponicsSaveDeviceState():
    connect.send_data_from_bound_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        gateway_id,
        num_messages,
        rsa_private_path,
        algorithm,
        ca_certs,
        mqtt_bridge_hostname,
        mqtt_bridge_port,
        jwt_expires_minutes,
        getDeviceStatePayload(),
    )
