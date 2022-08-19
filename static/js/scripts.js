// Disabling of the login button while at least on form field is empty
const inputFields = document.querySelectorAll('input[type="text"],input[type="password"]')
inputFields.forEach(field => {
    field.addEventListener('keyup', () => {
        const canSubmit = [...inputFields]
            .every(i => {
                return i.value
            });
        document.querySelector('input[type="submit"]').disabled = !canSubmit;
        })
    }
)