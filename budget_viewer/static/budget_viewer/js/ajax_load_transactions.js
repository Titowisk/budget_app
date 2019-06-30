$(document).ready(function(){

    let table // DataTable

    // query the html table
    let $table = $('#transactions_table').hide()

    let summary_filter = {
        "all": "[0-9]", // any string that contains numerals
        "income": "^[0-9]", // string that starts with a number
        "expense": "^-" // string ta starts with '-'
    }
    /**Year Click Event
     * When a year is clicked, it shows all months that have registered transactions
     */
    $('.year__item').click(function(e){
        let year = $(this).text()

        // slowly hide table
        $table.hide("slow")

        // clicking in a year button
        $.get(
            `transactions/monthsByYear/${year}`,
            function(data){
                // erase .options__months childs
                $('.options__months').empty()
    
                // takes a json data and fill up the .options__months element
                data.months.forEach(month => {
                    // build a li element with class, attribute and text
                    let $li = $('<li></li>').addClass('month__item').attr("data-id", month.id).text(`${month.name}`)
                    // append to the final of the .options_months element
                   $('.options__months').append($li)
                });
    
                // if table exists, destroy it
                if ( $.fn.dataTable.isDataTable( '#transactions_table' ) ) {
                    table.destroy()
                    // $('#transactions_table').empty()
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
                // load summary section
                loadSummarySection(data)
                // load table
                loadDataTable(data)
                
            }
        ).fail(function(){
            console.log("Não foi possível pegar os dados de transações do mês: " + month_id)
        })
    })

    /** Summary Filter Click Event */
    $('.summary__body > .summary__row').click(function(event){
        console.log(event.target)

        // only applies if table is visible (display != none)
        if ($table.css('display') != 'none') {

            // filter based on data-filter value
            // https://datatables.net/reference/api/column().search()
            $('#transactions_table').DataTable()
            .column(1)
            .search( summary_filter[$(event.target).attr('data-filter')], true, false )
            .draw()

            // show active filter
            // TODO
        }

    })

    /**
     * callback function used in $.get to load the DataTable  */ 
    let loadDataTable = (data) => {
        // show table
        $table.show()

        // load table using DataTable
        if ( $.fn.dataTable.isDataTable( '#transactions_table' ) ) {
            table.destroy() // if table exists, destroy it
        } 
        table = $table.DataTable({
            // "dom": "<l><t><ip>", // https://datatables.net/reference/option/dom // causes a bug for bootstrap 4 styling
            "searching": true,
            "data": JSON.parse(data.transactions),
            // https://datatables.net/reference/option/columns
            "columns": [
                // {"data": "fields.statement_number"},
                {"data": "fields.origin"},
                {"data": "fields.amount"},
                {"data": "fields.flow_method"},
                {"data": "fields.category"},
                // {"data": "fields.date"},
            ],
            // https://datatables.net/reference/option/columnDefs
            "columnDefs": [{
                "targets": 1,
                "createdCell": function (td, cellData, rowData, row, col) {
                    // change color for differenciation of incomes and expenses
                    if ( cellData < 0) {
                        $(td).css('color', '#B30000')
                    } else {
                        $(td).css('color', '#04B335')
                    }
                },
                
            }, 
                // https://datatables.net/manual/styling/classes
                {"targets": [1, 2], "className": "dt-body-center"}
            ]
        })
    }

    let loadSummarySection = (data) => {
        // load information from ajax data
        $('.summary__total').text(data.summary.summary_total)
        $('.summary__total_incomes').text(data.summary.incomes_total)
        $('.summary__total_expenses').text(data.summary.expenses_total)
    }
})    
