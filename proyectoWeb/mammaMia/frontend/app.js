var app = new Vue({
    el: '#app',
    data: {
        subtitle: '¡La mejor pizzería!',
        state: 'home',       
        historial: [], // Historial de vistas
        cargando: false,     
        busqueda: '',        
        
        // Datos
        pizzas: [],
        masas: [],
        ingredientes: [],
        
        // Filtros
        filtroMasa: '',         
        filtroIngredientes: [],

        // Selección
        itemSeleccionado: null 
    },
    
    mounted() {
        console.log("Iniciando App...");
        Promise.all([this.fetchMasas(), this.fetchIngredientes()])
            .then(() => {
                this.fetchPizzas(); 
            });
    },

    computed: {
        pizzasFiltradas: function() {
            if (!this.pizzas) return [];
            return this.pizzas.filter(pizza => {
                const coincideTexto = pizza.nombre.toLowerCase().includes(this.busqueda.toLowerCase());
                const coincideMasa = this.filtroMasa === '' || pizza.masa_id == this.filtroMasa;
                const coincideIngredientes = this.filtroIngredientes.length === 0 || 
                    this.filtroIngredientes.every(idSeleccionado => 
                        pizza.ingredientes_ids && pizza.ingredientes_ids.includes(idSeleccionado)
                    );
                return coincideTexto && coincideMasa && coincideIngredientes;
            });
        },

        pizzasDestacadas: function() {
            if (!this.pizzas) return [];
            const mejores = {}; 
            this.pizzas.forEach(pizza => {
                const masa = pizza.masa_nombre || 'Fina'; 
                const precio = parseFloat(pizza.precio);    
                if (!mejores[masa] || precio < parseFloat(mejores[masa].precio)) {
                    mejores[masa] = pizza; 
                }
            });
            return Object.values(mejores); 
        }
    },
    
    methods: {
        changeState: function(newState) {
            this.state = newState;
            if (newState !== 'menu' && !newState.startsWith('detalle')) {
                this.busqueda = '';
                this.filtroMasa = '';
                this.filtroIngredientes = [];
                this.historial = [];
                this.itemSeleccionado = null;
            }
            if (newState === 'masas' && this.masas.length === 0) this.fetchMasas();
            else if (newState === 'ingredientes' && this.ingredientes.length === 0) this.fetchIngredientes();
        },

        verDetalle: function(tipo, item) {
            this.historial.push({
                state: this.state,
                item: this.itemSeleccionado
            });

            this.itemSeleccionado = item;    
            this.state = 'detalle_' + tipo;  
            window.scrollTo(0,0);
        },

        volver: function() {
            if (this.historial.length > 0) {
                const pasoAnterior = this.historial.pop(); // Sacamos el último estado guardado
                this.state = pasoAnterior.state;
                this.itemSeleccionado = pasoAnterior.item; // Recuperamos la pizza (o masa) anterior
            } else {
                // Si no hay historial, volvemos al home por seguridad
                this.state = 'home';
                this.itemSeleccionado = null;
            }
        },

        // --- NUEVOS MÉTODOS DE NAVEGACIÓN CRUZADA ---
        irAMasa: function(masaId) {
            // Buscamos el objeto masa completo usando el ID
            const masaObj = this.masas.find(m => m.id == masaId);
            if (masaObj) {
                this.verDetalle('masa', masaObj);
            }
        },

        irAIngrediente: function(ingObj) {
            // Como ya tenemos el objeto ingrediente (viene del v-for), pasamos directo
            this.verDetalle('ingrediente', ingObj);
        },
        // ---------------------------------------------

        getIngredientesDePizza: function(pizza) {
            if (!pizza.ingredientes_ids) return [];
            return this.ingredientes.filter(ing => pizza.ingredientes_ids.includes(ing.id));
        },

        getPizzasConMasa: function(masaId) {
            return this.pizzas.filter(p => p.masa_id == masaId);
        },

        getPizzasConIngrediente: function(ingId) {
            return this.pizzas.filter(p => p.ingredientes_ids && p.ingredientes_ids.includes(ingId));
        },

        mostrarOferta: function() {
            Swal.fire({
                title: '¡Oferta Flash! ⚡',
                text: '2x1 en todas las pizzas con masa fina solo por hoy.',
                icon: 'info',
                confirmButtonText: '¡Genial!',
                confirmButtonColor: '#CD212A'
            });
        },

        // --- FETCHERS ---
        fetchPizzas: function() {
            this.cargando = true;
            fetch('http://127.0.0.1:8000/api/pizzas/')
                .then(res => { if(!res.ok) throw new Error(); return res.json(); })
                .then(data => { 
                    this.pizzas = data.map(p => {
                        let mId = (typeof p.masa === 'object' && p.masa !== null) ? p.masa.id : p.masa;
                        let mNombre = 'Fina';
                        if (this.masas.length > 0) {
                            const masaEnc = this.masas.find(m => m.id == mId);
                            if (masaEnc) mNombre = masaEnc.nombre;
                        }
                        let iIds = [];
                        if (Array.isArray(p.ingredientes)) {
                            iIds = p.ingredientes.map(i => (typeof i === 'object') ? i.id : i);
                        }
                        return { ...p, masa_id: mId, masa_nombre: mNombre, ingredientes_ids: iIds };
                    });
                    this.cargando = false; 
                })
                .catch(() => { this.cargarDemoPizzas(); });
        },
        fetchMasas: function() {
            return fetch('http://127.0.0.1:8000/api/masas/')
                .then(res => { if(!res.ok) throw new Error(); return res.json(); })
                .then(data => { this.masas = data; })
                .catch(() => { this.cargarDemoMasas(); });
        },
        fetchIngredientes: function() {
            return fetch('http://127.0.0.1:8000/api/ingredientes/')
                .then(res => { if(!res.ok) throw new Error(); return res.json(); })
                .then(data => { this.ingredientes = data; })
                .catch(() => { this.cargarDemoIngredientes(); });
        },

        // --- DATOS DEMO ---
        cargarDemoPizzas: function() {
            console.log("Cargando TUS PIZZAS (Local)");
            this.pizzas = [
                { id: 1, nombre: 'Margarita', descripcion: 'Clásica italiana con tomate y queso.', precio: '7.90', 
                    masa_nombre: 'Fina', masa_id: 1, vegetariana: false, ingredientes_ids: [2, 7, 8], imagen: 'media/pizzas/Margarita.png' },
                { id: 2, nombre: 'Jamón y Queso', descripcion: 'Suave y cremosa con jamón cocido.', precio: '8.20', 
                    masa_nombre: 'Fina', masa_id: 1, vegetariana: true, ingredientes_ids: [5, 7], imagen: 'media/pizzas/JamonYQueso.png' },
                { id: 3, nombre: 'Vegetal Mix', descripcion: 'Ligera y saludable con verduras frescas.', precio: '8.80', 
                    masa_nombre: 'Integral', masa_id: 3, vegetariana: true, ingredientes_ids: [1, 3, 4, 8], imagen: 'media/pizzas/Vegetal.png' },
                { id: 4, nombre: 'Mediterránea', descripcion: 'Inspirada en sabores del mediterráneo.', precio: '9.10', 
                    masa_nombre: 'Integral', masa_id: 3, vegetariana: false, ingredientes_ids: [1, 2, 5, 8], imagen: 'media/pizzas/Mediterranea.png' },
                { id: 5, nombre: 'Pepperoni Lovers', descripcion: 'Extra queso y extra pepperoni.', precio: '9.50', 
                    masa_nombre: 'Gordita', masa_id: 2, vegetariana: false, ingredientes_ids: [6, 7, 8], imagen: 'media/pizzas/Peperoni.png' },
                { id: 6, nombre: 'Cuatro Quesos', descripcion: 'Mezcla perfecta de quesos italianos.', precio: '10.00', 
                    masa_nombre: 'Gordita', masa_id: 2, vegetariana: true, ingredientes_ids: [7, 8], imagen: 'media/pizzas/CuatroQuesos.png' }
            ];
            this.cargando = false;
        },
        cargarDemoMasas: function() {
            this.masas = [
                { id: 1, nombre: 'Fina', descripcion: 'Masa fina y crujiente.', imagen: 'media/masas/MasaFina.png' },
                { id: 2, nombre: 'Gordita', descripcion: 'Masa gruesa estilo pan.', imagen: 'media/masas/MasaGordita.png' },
                { id: 3, nombre: 'Integral', descripcion: 'Masa de trigo integral.', imagen: 'media/masas/MasaIntegral.png' }
            ];
        },
        cargarDemoIngredientes: function() {
            this.ingredientes = [
                { id: 1, nombre: 'Aceitunas negras', descripcion: 'Sin hueso.', alergeno: false },
                { id: 2, nombre: 'Albahaca fresca', descripcion: 'Aromática y verde.', alergeno: false },
                { id: 3, nombre: 'Cebolla caramelizada', descripcion: 'Dulce y tostada.', alergeno: false },
                { id: 4, nombre: 'Champiñones', descripcion: 'Frescos y laminados.', alergeno: false },
                { id: 5, nombre: 'Jamón York', descripcion: 'Cocido y suave.', alergeno: true },
                { id: 6, nombre: 'Pepperoni', descripcion: 'Embutido especiado.', alergeno: true },
                { id: 7, nombre: 'Queso Mozzarella', descripcion: 'Queso auténtico italiano.', alergeno: true },
                { id: 8, nombre: 'Tomate', descripcion: 'Salsa de tomate natural.', alergeno: false }
            ];
        }
    }
});
