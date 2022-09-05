from django import forms as base_form


class CreateCollectionForm(base_form.Form):
    """_summary_

    Args:
        base_form (_type_): _description_
    """
    name = base_form.CharField(
        label="Collection Name",
        widget=base_form.TextInput(
                                    attrs={
                                        "placeholder": 'Enter your new collection name',
                                        }
                                )
        )
