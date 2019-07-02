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

    /** Edit Category Click Event
     * This is a Jquery event callback
     * @param {*} data 
    */
    const editCategoryEvent = (event) => {
        // console.log(`PK da linha clicada é ${event.data.rowData.pk}`)
        // console.log(`TD da categoria clicada é ${$(event.data.category_cell).text()}`)
        // add popover to all cells from category column 
        let current_category_cell = event.data.category_cell                       
        let popover_template = `
        <div class="popover" role="tooltip">
            <div class="arrow"></div>
            <h3 class="popover-header d-flex justify-content-between"></h3>
            <div class="popover-body">
                
            </div>
        </div>
        `
        // https://getbootstrap.com/docs/4.3/components/popovers/#usage
        $(current_category_cell).popover({
            "template": popover_template,
            "content": `
            <form action="CategoryFormView" method="post">
                <select class="custom-select">
                    <option selected>Open this select menu</option>
                    <option value="cat1">cat1</option>
                    <option value="cat2">cat2</option>
                    <option value="cat3">cat3</option>
                </select>
                <button type="submit" class="btn btn-primary btn-sm">Editar esta</button>
                <button type="submit" class="btn btn-primary btn-sm">Editar similares </button>
            </form>
            `,
            "title": `Editar Categoria <span class="close-edit-category" aria-hidden="true">&times;</span>`,
            "placement": "left",
            "html": true,
            "trigger": "manual"
        })

        $(current_category_cell).popover('toggle')

        // $(event.data.category_cell).popover('show')
        // add form widget inside (GET?)

        // wait for user input

        // handle user submit (POST)

        // return message or error
    }

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
            // https://datatables.net/reference/option/rowId
            "rowId": "pk",
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
            "columnDefs": [
                // change color for differenciation of incomes and expenses
                {
                    "targets": 1,
                    "createdCell": function (td, cellData, rowData, row, col) {

                        if ( cellData < 0) {
                            $(td).css('color', '#B30000')
                        } else {
                            $(td).css('color', '#04B335')
                        }
                    },
                
                }, 
                // https://datatables.net/manual/styling/classes
                // center align
                {
                    "targets": [1, 2, 3], 
                    "className": "text-center"
                },
                {
                    "targets": 3,
                    "createdCell": function (td, cellData, rowData, row, col) {
                        
                        // Add click event and passes rowData to event.data
                        $(td).click({rowData, "category_cell": td}, editCategoryEvent)
                        
                    }
                }
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
