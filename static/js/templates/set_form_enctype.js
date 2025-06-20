document.addEventListener('DOMContentLoaded', function () {
  console.log('✅ DOMContentLoaded');
  const form = document.querySelector('#representante_form');
	console.log('✅ Form found:', form);
  if (form) {
    form.setAttribute('enctype', 'multipart/form-data');
    console.log('✅ Form enctype set to multipart/form-data');
  }
});