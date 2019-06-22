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
    if (!$.fn.dataTable.isDataTable('#transactions_table')) {
        table = $('#transactions_table').DataTable({
            "serverSide": true,
            "paging": true,
            "ajax": {
                "url": `transactions/transactionsByMonth/${month_id}`,
            }
    
        })
    } 
    // DID NOT WORK: its not worth trying this, no easy answears on internet
    // else {
    //     table.clear()
    //     table = table.ajax.url( `transactions/transactionsByMonth/${month_id}` )
    //     table.ajax.reload()
    // }
    
})

// TODO: function that create textinput filtering for "origin" and "type"
// TODO: function that create selectinput for "amount" options = ['all', 'incomes', 'expenses']

