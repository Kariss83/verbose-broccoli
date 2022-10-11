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


// Using cam on viewer device
function getCurrentURL () {
    return window.location.href
  }

const url = getCurrentURL()

if (url.endsWith('/barcode/upload/')){
    const webCamElement = document.getElementById('webCam');
    const canvasElement = document.getElementById('webCamCanvas');
    const webcam = new Webcam(webCamElement, "user", canvasElement);
    const cameraElement = document.querySelector('#my-camera')
    const notAuthorizedElement = document.querySelector('.not-yet-authorized')
    const scanButtonElement = document.querySelector('#scan-button')
    const imageDataInput = document.querySelector('#image-data')
    const scanForm = document.querySelector("form[name='scanform']")
    
    const startWebCam = () => {
        webcam.start()
            .then(result =>{
                // webCamElement.style = ""
                console.log("webcam started");
            })
            .catch(err => {
                console.log(err);
            });
        }
    
    const takePicture = () => {
        let picture = webcam.snap();
        imageDataInput.value = picture;
    }
    
    cameraElement.addEventListener("click", () => {
        notAuthorizedElement.classList.add('d-none');
        startWebCam();
    })
    
    scanButtonElement.addEventListener("click", (e) => {
        e.preventDefault();
        takePicture();
        scanForm.requestSubmit(scanButtonElement);
    })

    webCamElement.addEventListener("click", (e) =>{
        e.preventDefault();
        webcam.flip();
        webcam.start()
    })
}

