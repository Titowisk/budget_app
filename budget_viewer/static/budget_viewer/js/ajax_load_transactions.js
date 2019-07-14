/**
 * 1 - loadDataTable - loads the table and adds a click event to each category cell
 *     $(td).click({rowData, "category_cell": td}, editCategoryEvent)
 * 2 - editCategoryEvent  - creates a popover (addPopover) with a select dropdown ($.get) and two buttons
 *     $.get() - populates the dropdown with a GET to the server
 * 3 - When the GET is done, creates a click event for the buttons ($('.popover__buttons').click)
 * 4 - $('.popover__buttons').click creates a POST to change data on the server
 */

$(document).ready(function(){

    let year, month_id, table

    // query the html table
    let $table = $('#transactions_table').hide()

    let summary_filter = {
        "all": "[0-9]", // any string that contains numerals
        "income": "^[0-9]", // string that starts with a number
        "expense": "^-" // string ta starts with '-'
    }

    // TODO: encapsulate it in a async function
    /**Year Click Event
     * When a year is clicked, it shows all months that have registered transactions
     */
    $('.year__item').click(function(e){
        year = $(this).text()

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
    
    // TODO: encapsulate it in a async function
    /** Month Click Event
     * Show all registered transactions of the selected month
     */
    $('.options__months').click(function(e){  
    
        month_id = $(e.target).attr('data-id')
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

    /** Function Add Popover 
     *  
     * @param {*} event 
     */
    const addPopover = (select_form, event_data) => {
        // create popover body
        let popover_content = `
            ${select_form}
            <div class="popover__buttons">
                <button id="btn_edit_this" type="submit" class="btn btn-primary btn-sm">Editar esta</button>
                <button id="btn_edit_similars" type="submit" class="btn btn-primary btn-sm">Editar similares </button>
            </div>
        `
        // add popover to all cells from category column 
        let current_category_cell = event_data.category_cell                       
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
            "content": popover_content,
            "title": `Editar Categoria <span class="close-edit-category" aria-hidden="true">&times;</span>`,
            "placement": "left",
            "html": true,
            "trigger": "manual"
        })

        $(current_category_cell).popover('toggle')
    }

    /** Edit Category Click Event
     * This is a Jquery event callback
     * 
     * @param {} event
     * event.data.rowData.pk = primary key of the transaction line
     * event.data.category_cell = element <td> from the category clicked
    */
    const editCategoryEvent = (categoryEvent) => {
  
        // add form widget inside popover (GET?)
        let editCategoryForm
        $.get(
            // url
            `transactions/edit-category/${categoryEvent.data.rowData.pk}`,
            function(html_select_form){
                addPopover(html_select_form, categoryEvent.data)
            }
        )
        .fail(function(){
            // TODO: handle error messages
            alert("Ocorreu uma falha na busca de opções de categorias")
        })
        .done(function(){
            // TODO: update buttons only are enabled if user change select input
       
            // wait for user input
            $('.popover__buttons').click(function(event){
                console.log( event.target )
                let data
                if ( event.target.id == "btn_edit_this") {
                    // edit only the selected transaction
                    data = 'this'
                    
                } else if (event.target.id == "btn_edit_similars") {
                    // edit all transactions with similar origin
                    data = 'similars'
                }
                
                // https://docs.djangoproject.com/en/dev/ref/csrf/#acquiring-csrf-token-from-html
                // https://api.jquery.com/jquery.ajax/#jQuery-ajax-settings
                // makes a POST request based on the button clicked
                $.post({
                    "url": `transactions/edit-category/${categoryEvent.data.rowData.pk}`,
                    "beforeSend": function(xhr, settings) {
                        let csrftoken = $("[name=csrfmiddlewaretoken]").val(); // THIS IS NOT SAFE!!!
                        if (!this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    "data": {
                        "data": data, 
                        "newCategoryName": $('#edit-category-select').val()
                    },
                    "success": function(data, textStatus, jqXHR ){
                        // TODO
                        alert(data)
                    },
                    "error": function( jqXHR, textStatus, errorThrown) {
                        alert(errorThrown)
                    }
                })
                // return message or error
                .fail(function() {
                    // TODO
                    alert("Não foi possível atualizar a categoria da(s) transação(ões).")
                })
                .done(function(){

                    // closes the popover TODO
                    $('.popover').popover('hide')

                    // reloads the table TODO
                    $(`.month__item[data-id=${month_id}]`).trigger('click')
                })
            })

            

        })
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
