export async function predictCalories(image, portion) {
  const formData = new FormData();
  formData.append("file", image);
  formData.append("portion", portion);

  const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    body: formData,
  });

  return await res.json();
}
