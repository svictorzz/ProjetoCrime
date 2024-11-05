document.getElementById('insertForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const nome = document.getElementById('nome').value;
    const bairro = document.getElementById('bairro').value;
    const regiao = document.getElementById('regiao').value;
    const incidencias = document.getElementById('incidencias').value.split(',').reduce((acc, item) => {
        const [crime, count] = item.split(':');
        acc[crime.trim()] = parseInt(count.trim());
        return acc;
    }, {});
    
    fetch('/inserir_dados', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nome: nome,
            bairro: bairro,
            regiao: regiao,
            incidencia: incidencias
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        document.getElementById('insertForm').reset();
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});

document.getElementById('fetchData').addEventListener('click', function() {
    fetch('/pesquisar?tipo=roubo')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('dataContainer');
            container.innerHTML = '';
            data.forEach(item => {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${item.nome}</strong> (${item.bairro}, ${item.regiao}): ${JSON.stringify(item.incidencia)}`;
                container.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Erro:', error);
        });
});
