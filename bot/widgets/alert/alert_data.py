from aiogram_dialog import DialogManager


def generate_alert_data(manager: DialogManager):
    return {
        "alert_title": manager.dialog_data.get("alert_title", None),
        "alert_description": manager.dialog_data.get("alert_description", None),
        "alert_back_button_text": manager.dialog_data.get("alert_back_button_text", None),
        "alert_process_button_text": manager.dialog_data.get("alert_process_button_text", None),

        "alert_handler": manager.dialog_data.get("alert_handler", None),
        "alert_previous_state": manager.dialog_data.get("alert_previous_state", None)
    }
