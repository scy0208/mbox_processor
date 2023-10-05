import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_all_labels(service):
    """
    Fetch all labels along with their metadata for the authenticated Gmail account.
    
    Parameters:
    - service: Authenticated Gmail API service instance.
    
    Returns:
    - List of dictionaries containing label metadata.
    """
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return labels


def delete_all_custom_labels(service):
    """
    Delete all custom labels in the authenticated Gmail account.
    
    Parameters:
    - service: Authenticated Gmail API service instance.
    """
    # Get all labels
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    # List of Gmail system labels you might not want to delete
    system_labels = [
        'INBOX', 'SPAM', 'TRASH', 'UNREAD', 'STARRED', 'IMPORTANT',
        'SENT', 'DRAFT', 'CATEGORY_PERSONAL', 'CATEGORY_SOCIAL',
        'CATEGORY_UPDATES', 'CATEGORY_FORUMS', 'CATEGORY_PROMOTIONS',
        'CHAT'  # Adding CHAT to the list
    ]
    
    for label in labels:
        if label['name'].upper() not in system_labels:
            try:
                service.users().labels().delete(userId='me', id=label['id']).execute()
                print(f"Deleted label: {label['name']}")
            except HttpError as e:
                print(f"Unable to delete label: {label['name']}. Reason: {e}")



def create_label(service, label_name, background_color="#FFFFFF"):
    """
    Create a Gmail label with the specified name and background color.
    
    Parameters:
    - service: Authenticated Gmail API service instance.
    - label_name: Name of the label to be created.
    - background_color: Background color for the label (default is white).
    
    Returns:
    - ID of the created label.
    """
    new_label = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show',
        'color': {
            'backgroundColor': background_color,
            'textColor': '#FFFFFF'  # Default text color is black
        }
    }
    created_label = service.users().labels().create(userId='me', body=new_label).execute()
    return created_label['id']

def create_labels(service):
    """
    Create labels given a dictionary mapping label names to their colors.
    
    Parameters:
    - service: Authenticated Gmail API service instance.
    
    Returns:
    - Dictionary mapping label names to their corresponding label IDs.
    """
    label_colors = {
        'KOL承诺发内容': '#6d9eeb',   # Blue
        '其他KOL话题': '#0b804b',         # Green
        'KOL问粉丝折扣码': '#f691b3',           # Pink
        '发错货补发': '#cc3a21',         # Red
        'KOL已发内容': '#6d9eeb',    # Blue
        '订单信息更新': '#cc3a21',        # Red
        '广告': '#999999',          # Gray
        '取消订单': '#cc3a21',             # Red
        '其他差评': '#f691b3',   # Pink
        '设计差评': '#cf8933',          # Orange
        '其他客服话题': '#cf8933',   # Orange
        'KOL同意不收费合作': '#6d9eeb', # Blue
        '尺寸差评': '#cf8933',        # Orange
        '好评': '#0b804b',         # Green
        '首次提出退货': '#cc3a21',        # Red
        '坚持要求退货': '#cc3a21',        # Red
        '社交媒体互动奖励': '#0b804b',     # Green
        'KOL需要付费合作': '#a479e2',   # Purple
        '询问发货': '#0b804b',           # Green
        '服务商邮件': '#999999',            # Gray
        '质量差评': '#cf8933'          # Orange
    }

    created_labels = {}
    for label, color in label_colors.items():
        label_id = create_label(service, label, color)
        created_labels[label] = label_id

    return created_labels


def main():
    print(create_labels(get_service()))

if __name__ == '__main__':
    main()
