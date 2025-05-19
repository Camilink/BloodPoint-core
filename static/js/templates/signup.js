
document.addEventListener('DOMContentLoaded', () => {
	const rutField = document.querySelector('#rut_representante')
	if (rutField) { rutField.addEventListener('input', (event) => {
		formatearCampoRUT(event.target)
	})}
})

const formatearCampoRUT = (input) => {
	// Obtener valor actual sin puntos ni guiones
	let rut = input.value.replace(/\./g, '').replace(/-/g, '');
	// Si está vacío, no hacer nada
	if (rut.length === 0) return;
	// Separar número y dígito verificador
	let dv = rut.slice(-1);
	let numero = rut.slice(0, -1);
	// Formatear con puntos
	numero = numero.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
	// Asignar valor formateado
	input.value = numero + "-" + dv;
}

const validarFormulario = () => {
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;
    const rut = document.getElementById('rut_representante').value;
    const email = document.getElementById('email').value;
    // Validar que las contraseñas coincidan
    if (password1 !== password2) {
			alert('Las contraseñas no coinciden');
			return false;
    }
    // Validar que la contraseña tenga al menos 8 caracteres
    if (password1.length < 8) {
			alert('La contraseña debe tener al menos 8 caracteres');
			return false;
    }
    // Validar formato de RUT chileno básico (puedes mejorar esta validación)
    const rutRegex = /^[0-9]{1,2}.[0-9]{3}.[0-9]{3}-[0-9kK]{1}$/;
    if (!rutRegex.test(rut)) {
			alert('Formato de RUT inválido. Use formato: 12.345.678-K');
			return false;
    }
    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
			alert('Formato de email inválido');
			return false;
    }
    return true;
}
