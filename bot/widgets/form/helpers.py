def use_models(model: dict):
    model_buttons = []
    id = 0

    for item_key, item_value in model.items():
        id += 1

        model_buttons.append((id, model.get(item_key)["title"]))
        model.get(item_key).update({
            "id": id,
            "value": model.get(item_key)["default"]
        })

    return model, model_buttons, id
