document.addEventListener('DOMContentLoaded', function() {

    const linksPizza = document.querySelectorAll('.pizza-link');
    
    linksPizza.forEach(link => {
        link.addEventListener('click', function(e) {
            console.log("Click en pizza detectado");
        });
    });

    const buscadorInput = document.getElementById('buscador-cliente');
    
    if (buscadorInput) {
        buscadorInput.addEventListener('keyup', function(e) {
            const termino = e.target.value.toLowerCase();
            const pizzas = document.querySelectorAll('.pizza');

            pizzas.forEach(pizza => {
                const titulo = pizza.querySelector('h2').textContent.toLowerCase();
                if (titulo.includes(termino)) {
                    pizza.style.display = 'block';
                    pizza.style.opacity = '1';
                    pizza.style.transform = 'scale(1)';
                } else {
                    pizza.style.display = 'none';
                }
            });
        });
    }

    const btnOferta = document.getElementById('btn-oferta');
    
    if (btnOferta) {
        btnOferta.addEventListener('click', function() {
            
            fetch('/api/oferta/')
                .then(response => response.json())
                .then(data => {
                    Swal.fire({
                        title: '¡Oferta Flash! ⚡',
                        text: data.mensaje,
                        icon: 'info',
                        confirmButtonText: '¡Genial!',
                        confirmButtonColor: '#CD212A'
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire('Error', 'No se pudo cargar la oferta', 'error');
                });
        });
    }
});