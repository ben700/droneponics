from cryptography.fernet import Fernet

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        
    # encrypt data
    encrypted_data = f.encrypt(file_data)  
        
    # write the encrypted file
    with open(str(filename + "_encrypted"), "wb") as file:
        file.write(encrypted_data)
        
def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(str(filename + "_encrypted"), "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
        
def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()        


def createDevice():
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # certificate_file = 'path/to/certificate.pem'

    client = iot_v1.DeviceManagerClient()

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [
            {
                "public_key": {
                    "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                    "key": certificate,
                }
            }
        ],
    }
    return client.create_device(request={"parent": parent, "device": device_template})

def patchDevice():
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # public_key_file = 'path/to/certificate.pem'
    print("Patch device with RSA256 certificate")

    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    public_key_bytes = ""
    with io.open(public_key_file) as f:
        public_key_bytes = f.read()

    key = iot_v1.PublicKeyCredential(
        format=iot_v1.PublicKeyFormat.RSA_X509_PEM, key=public_key_bytes
    )

    cred = iot_v1.DeviceCredential(public_key=key)
    device = client.get_device(request={"name": device_path})

    device.id = b""
    device.num_id = 0
    device.credentials.append(cred)

    mask = gp_field_mask.FieldMask()
    mask.paths.append("credentials")

    return client.update_device(request={"device": device, "update_mask": mask})
        
def getDevice():
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    print("Getting device")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    # See full list of device fields: https://cloud.google.com/iot/docs/reference/cloudiot/rest/v1/projects.locations.registries.devices
    # Warning! Use snake_case field names.
    field_mask = gp_field_mask.FieldMask(
        paths=[
            "id",
            "name",
            "num_id",
            "credentials",
            "last_heartbeat_time",
            "last_event_time",
            "last_state_time",
            "last_config_ack_time",
            "last_config_send_time",
            "blocked",
            "last_error_time",
            "last_error_status",
            "config",
            "state",
            "log_level",
            "metadata",
            "gateway_config",
        ]
    )
    
    device = client.get_device(request={"name": device_path, "field_mask": field_mask})

    print("Id : {}".format(device.id))
    print("Name : {}".format(device.name))
    print("Credentials:")

    if device.credentials is not None:
        for credential in device.credentials:
            keyinfo = credential.public_key
            print("\tcertificate: \n{}".format(keyinfo.key))

            if keyinfo.format == 4:
                keyformat = "ES256_X509_PEM"
            elif keyinfo.format == 3:
                keyformat = "RSA_PEM"
            elif keyinfo.format == 2:
                keyformat = "ES256_PEM"
            elif keyinfo.format == 1:
                keyformat = "RSA_X509_PEM"
            else:
                keyformat = "UNSPECIFIED_PUBLIC_KEY_FORMAT"
            print("\tformat : {}".format(keyformat))
            print("\texpiration: {}".format(credential.expiration_time))

    print("Config:")
    print("\tdata: {}".format(device.config.binary_data))
    print("\tversion: {}".format(device.config.version))
    print("\tcloudUpdateTime: {}".format(device.config.cloud_update_time))

    return device



# uncomment this if it's the first time you run the code, to generate the key
write_key()
# load the key
key = load_key()
# file name
file = "data.csv"
# encrypt it
encrypt(file, key)

# decrypt the file
decrypt(file, key)


print("Success : File saved to disk")
