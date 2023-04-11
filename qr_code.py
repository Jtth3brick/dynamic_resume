import qrcode
import yaml

def create_qr_code(yaml_name):
    # Load YAML file
    with open(yaml_name, 'r') as f:
        resume_yaml = yaml.safe_load(f)
    # Get QR code link and dimension
    qr_link = resume_yaml['qr']['link']
    qr_dim = resume_yaml['qr']['dim']
    # Generate QR code using qrcode library
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=4)
    qr.add_data(qr_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Resize image to specified dimensions
    img = img.resize((qr_dim, qr_dim))
    # Save QR code as PNG file
    img.save('qr.png', format='png')