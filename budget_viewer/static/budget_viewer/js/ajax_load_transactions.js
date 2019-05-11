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
            console.log(data.transactions)
            // erase previous data
            $('.budget__body').empty()

            // takes json data and fill up the each budget__cell
            JSON.parse(data).forEach(transaction => {
                let $tr = $('<tr></tr>').addClass('budget__row')
                
                let $td_statement_number = $('<td></td>').addClass('budget__cell budget__statement_number').text(transaction.fields.statement_number)
                let $td_date = $('<td></td>').addClass('budget__cell budget__date').text(transaction.fields.date)
                let $td_flow_method = $('<td></td>').addClass('budget__cell budget__flow_method').text(transaction.fields.flow_method)
                let $td_origin = $('<td></td>').addClass('budget__cell budget__origin').text(transaction.fields.origin)
                let $td_amount
                if (parseFloat(transaction.fields.amount) >= 0) {
                    $td_amount = $('<td></td>').addClass('budget__cell budget__amount budget__amount--income').text(transaction.fields.amount)
                } else {
                    $td_amount = $('<td></td>').addClass('budget__cell budget__amount budget__amount--expense').text(transaction.fields.amount)
                }

                $tr.append($td_statement_number, $td_date, $td_flow_method, $td_origin, $td_amount)
                $('.budget__body').append($tr)
            })
            
        }
    ).fail(function(){
        console.log("Não foi possível pegar os dados de transações do mês: " + month_id)
    })
})


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
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1073,
//         "fields": {
//             "statement_number": "0225467",
//             "origin": "Groove Bar",
//             "amount": "-30.00",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1074,
//         "fields": {
//             "statement_number": "0260498",
//             "origin": "Shopping da Bahia",
//             "amount": "-6.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1075,
//         "fields": {
//             "statement_number": "0796962",
//             "origin": "Tokai",
//             "amount": "-19.84",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1076,
//         "fields": {
//             "statement_number": "0855457",
//             "origin": "Mariposa",
//             "amount": "-31.80",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1077,
//         "fields": {
//             "statement_number": "0884224",
//             "origin": "Salvador Gestao d",
//             "amount": "-8.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1078,
//         "fields": {
//             "statement_number": "0411992",
//             "origin": "00039872 04111819",
//             "amount": "-200.00",
//             "flow_method": " sq c/c Bco24h",
//             "date": "0018-11-05"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1079,
//         "fields": {
//             "statement_number": "0060883",
//             "origin": "Ponto Verde Supermer",
//             "amount": "-20.96",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-06"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1080,
//         "fields": {
//             "statement_number": "0240465",
//             "origin": "Rota Park Bahia Esta",
//             "amount": "-7.44",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-06"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1081,
//         "fields": {
//             "statement_number": "0142536",
//             "origin": "Lanchonete Divino sa",
//             "amount": "-6.00",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-07"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1082,
//         "fields": {
//             "statement_number": "0011451",
//             "origin": "Facilita",
//             "amount": "-14.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-08"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1083,
//         "fields": {
//             "statement_number": "0888116",
//             "origin": "Salvador Gestao d",
//             "amount": "-7.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-08"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1084,
//         "fields": {
//             "statement_number": "0460215",
//             "origin": "Marineuza Rabelo Ribeiro",
//             "amount": "1000.00",
//             "flow_method": " Dep Transf Bdn",
//             "date": "0018-11-09"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1085,
//         "fields": {
//             "statement_number": "6018170",
//             "origin": "Ludmila Rosas de Santana",
//             "amount": "-35.00",
//             "flow_method": " Transf Autoriz",
//             "date": "0018-11-09"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1086,
//         "fields": {
//             "statement_number": "0184588",
//             "origin": "Shopping da Bahia",
//             "amount": "-6.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-09"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1087,
//         "fields": {
//             "statement_number": "0417342",
//             "origin": "Lanche Salvador",
//             "amount": "-5.00",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-09"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1088,
//         "fields": {
//             "statement_number": "0101008",
//             "origin": "Ponto Verde Supermer",
//             "amount": "-23.47",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1089,
//         "fields": {
//             "statement_number": "0110297",
//             "origin": "Organico Comercial",
//             "amount": "-26.82",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1090,
//         "fields": {
//             "statement_number": "0198798",
//             "origin": "Freddo",
//             "amount": "-11.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1091,
//         "fields": {
//             "statement_number": "0413921",
//             "origin": "Posto Chamine",
//             "amount": "-100.00",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1092,
//         "fields": {
//             "statement_number": "0486464",
//             "origin": "Freddo",
//             "amount": "-8.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1093,
//         "fields": {
//             "statement_number": "0885473",
//             "origin": "Salvador Gestao d",
//             "amount": "-8.50",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-12"
//         }
//     }, {
//         "model": "bank_statements_reader.transaction",
//         "pk": 1094,
//         "fields": {
//             "statement_number": "0974000",
//             "origin": "Lanche Salvador",
//             "amount": "-5.00",
//             "flow_method": " Visa Electron",
//             "date": "0018-11-13"
//         }
//     },