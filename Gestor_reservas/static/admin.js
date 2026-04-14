/*dejamos esto para que lea y compare el archivo que se le sube
<script>
    let miGrafico;

    document.getElementById('csvInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(event) {
            const contenido = event.target.result;
            // Dividimos por líneas y quitamos las vacías
            const lineas = contenido.split(/\r?\n/).filter(line => line.trim() !== "");
            
            // contar reservas de entrada
            const conteoOcupacion = {};

            // saltar el encabezado del CSV
            for (let i = 1; i < lineas.length; i++) {
                // Separamos por coma (tu archivo usa comas según las imágenes)
                const columnas = lineas[i].split(',');

                // indice de fecha de entrada
                if (columnas.length >= 4) {
                    const fechaEntrada = columnas[3].trim();
                    
                    if (fechaEntrada) {
                        // Si la fecha ya existe, sumamos 1 huésped; si no, empezamos en 1
                        conteoOcupacion[fechaEntrada] = (conteoOcupacion[fechaEntrada] || 0) + 1;
                    }
                }
            }

            //datos a chart
            // orden por fecha
            const etiquetasFechas = Object.keys(conteoOcupacion).sort();
            
            // calculo por porcentaje de ocupacion segun las entradas
            const datosPorcentaje = etiquetasFechas.map(fecha => {
                const numHuespedes = conteoOcupacion[fecha];
                return ((numHuespedes / 50) * 100).toFixed(1);
            });

            if (etiquetasFechas.length > 0) {
                renderizarGraficoTendencia(etiquetasFechas, datosPorcentaje);
            } else {
                alert("No se encontraron fechas de entrada válidas en el archivo.");
            }
        };
        reader.readAsText(file);
    });

    function renderizarGraficoTendencia(labels, data) {
        const ctx = document.getElementById('graficoFinanzas').getContext('2d');
        
        // borra el grafico anterior para no generar errores
        if (miGrafico) { 
            miGrafico.destroy(); 
        }

        miGrafico = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels, // Fechas extraídas columna 4 del CSV
                datasets: [{
                    label: 'Ocupación por Fecha de Entrada',
                    data: data, // Porcentajes calculados
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    fill: true,
                    tension: 0.4, 
                    pointRadius: 6,
                    pointBackgroundColor: '#4e73df',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100, // Siempre tope de 100%
                        ticks: { callback: value => value + '%' }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: context => `Ocupación: ${context.parsed.y}%`
                        }
                    }
                }
            }
        });
    }
</script>
*/