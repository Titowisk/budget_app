let table
/**Year Click Event
 * When a year is clicked, it shows all months that have registered transactions
 */
$('.year__item').click(function(e){
    let year = $(this).text()
    // clicking in a year button
    $.get(
        `transactions/monthsByYear/${year}`,
        function(data){
            console.log(data.months)

            // erase .options__months childs
            $('.options__months').empty()

            // takes a json data and fill up the .options__months element
            data.months.forEach(month => {
                // build a li element with class, attribute and text
                let $li = $('<li></li>').addClass('month__item').attr("data-id", month.id).text(`${month.name}`)
                // append to the final of the .options_months element
               $('.options__months').append($li)
            });

            if ( $.fn.dataTable.isDataTable( '#transactions_table' ) ) {
                table.destroy()
                $('#transactions_table').empty()
            } 
        }

    ).fail(function(){
        // TODO: handle error messages
        alert("Ocorreu uma falha na busca dos meses do ano escolhido.")
    })
})

/** Month Click Event
 * Show all registered transactions of the selected month
 */
$('.options__months').click(function(e){  

    let month_id = $(e.target).attr('data-id')
    $.get(`transactions/transactionsByMonth/${month_id}`,
        function(data){
                       
            // query the table
            let $table = $('#transactions_table')

            // erase previous data
            $table.empty()

            // build table header and footer
            $thead = $('<thead></thead>')
            $tr = $('<tr></tr>')
            // $tr.append('<th>Numero do Documento</th>')
            $tr.append('<th>Origem</th>')
            $tr.append('<th>Quantidade</th>')
            $tr.append('<th>Tipo</th>')
            // $tr.append('<th>Data</th>')
            $thead.append($tr)
            
            $tfoot = $('<tfoot></tfoot>')
            $tr = $('<tr></tr>')
            // $tr.append('<td>Numero do Documento</td>')
            $tr.append('<td>Origem</td>')
            $tr.append('<td>Quantidade</td>')
            $tr.append('<td>Tipo</td>')
            // $tr.append('<td>Data</td>')
            $tfoot.append($tr)

            $table.append($thead)
            $table.append($tfoot)

            // load table using DataTable
            if ( $.fn.dataTable.isDataTable( '#transactions_table' ) ) {
                table.destroy()
            } 
            table = $table.DataTable({
                "dom": "<'column_filter'l><t><ip>", // https://datatables.net/reference/option/dom
                "data": JSON.parse(data),
                "columns": [
                    // {"data": "fields.statement_number"},
                    {"data": "fields.origin"},
                    {"data": "fields.amount"},
                    {"data": "fields.flow_method"},
                    // {"data": "fields.date"},
                ]
            })           
            
        }
    ).fail(function(){
        console.log("Não foi possível pegar os dados de transações do mês: " + month_id)
    })
})

// TODO: function that create textinput filtering for "origin" and "type"
let textInputFilter = (colIndex) => {}
// TODO: function that create selectinput for "amount" options = ['all', 'incomes', 'expenses']


// [{
//         "model": "bank_statements_reader.transaction",
//         "pk": 1071,
//         "fields": {
//             "statement_number": "0000094",
//             "origin": "Unifacs Novembro",
//             "amount": "-1029.06",
//             "flow_method": " Pagto Cobranca",
//             "date": "0018-11-01"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1072,
//         "fields": {
//             "statement_number": "0156786",
//             "origin": "Tagarelli",
//             "amount": "-18.86",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, 
//      ...