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
        }

    ).fail(function(){
        console.log("YOU DIED! :(")
    })
})

$('.options__months').click(function(e){  

    let month_id = $(e.target).attr('data-id')
    $.get(`transactions/transactionsByMonth/${month_id}`,
        function(data){
            console.log(data)
            // erase previous data
            $('.budget__body').empty()

            // takes json data and fill up the each budget__cell
            data.transactions.forEach(transaction => {
                let $tr = $('<tr></tr>').addClass('budget__row')
                
                let $td_statement_number = $('<td></td>').addClass('budget__cell budget__statement_number').text(transaction.fields.statement_number)
                let $td_date = $('<td></td>').addClass('budget__cell budget__date').text(transaction.fields.date)
                let $td_flow_method = $('<td></td>').addClass('budget__cell budget__flow_method').text(transaction.fields.flow_method)
                let $td_origin = $('<td></td>').addClass('budget__cell budget__origin').text(transaction.fields.origin)
                let $td_amount
                if (parseFloat(amount) >= 0) {
                    $td_amount = $('<td></td>').addClass('budget__cell budget__amount budget__amount--income').text(transaction.fields.amount)
                } else {
                    $td_amount = $('<td></td>').addClass('budget__cell budget__amount budget__amount--expense').text(transaction.fields.amount)
                }

                $tr.append($td_statement_number, $td_date, $td_flow_method, $td_origin, $td_amount)
            })
            
        }
    ).fail(function(){
        console.log("Não foi possível pegar os dados de transações do mês: " + month_id)
    })
})