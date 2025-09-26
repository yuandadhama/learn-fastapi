const form = document.getElementById("input-student");
const url = 'http://127.0.0.1:8000/create-student/'

const sendData =  async () => {
  const formData = new FormData(form);

  const student = {
    name: formData.get("name"),
    age: parseInt(formData.get("age")),
    year: formData.get("year")
  }

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(student)
    });
    
    const data = await response.json();
    console.log(data);
  } catch (e) {
    console.log("error")
    console.error(e)
  }
} 

form.addEventListener('submit', e => {
  e.preventDefault();
  sendData();
})