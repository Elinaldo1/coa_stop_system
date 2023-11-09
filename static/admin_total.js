
document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.results');
    const rows = table.querySelectorAll('tbody tr');
    let total = 0;

    rows.forEach(function(row) {
        const quantidadeCell = row.querySelector('.field-quantidade');  // Índice da coluna 'quantidade'
        if (quantidadeCell) {
            const quantidade = parseFloat(quantidadeCell.textContent.trim());
            if (!isNaN(quantidade)) {
                total += quantidade;
                // alert(total)
            }
        }
    });

    const totalRow = document.createElement('tr');
    totalRow.innerHTML = `
        <td></td>
        <td>
            <h3>
            Total:
            </h3>
        </td>
        <td>
            <h3>
            ${total}
            </h3>
        </td>
    `;
    
    table.querySelector('tbody').appendChild(totalRow);

    const header = document.getElementById('header').nextElementSibling
    const backgroundColorHeader = window.getComputedStyle(header.querySelector('div')).background

    const container = document.getElementById('content')
    const qtdProdutoElement = document.createElement('div');
    qtdProdutoElement.setAttribute('class', 'qtdProdutoElement');
    qtdProdutoElement.textContent = total
    qtdProdutoElement.style.background = backgroundColorHeader
    container.insertBefore(qtdProdutoElement, document.getElementById('content-main'))
});
