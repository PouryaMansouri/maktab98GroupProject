jQuery(document).ready(function ($) {
    'use strict';

    if ($("table.first").length) {

        $(document).ready(function () {
            $('table.first').DataTable();
        });
    }

    /* Calender jQuery **/

    if ($("table.second").length) {

        $(document).ready(function () {
            var table = $('table.second').DataTable({
                lengthChange: true,
                // buttons: ['copy', 'excel', 'pdf', 'print', 'colvis']
                buttons: [
                    {
                        extend: 'copy',
                        exportOptions: {
                            columns: ':visible:not(.no-export)'
                        }
                    },
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible:not(.no-export)'
                        }
                    },
                    {
                        extend: 'pdf',
                        exportOptions: {
                            columns: ':visible:not(.no-export)'
                        }
                    },
                    {
                        extend: 'print',
                        exportOptions: {
                            columns: ':visible:not(.no-export)'
                        }
                    },
                    {
                        extend: 'colvis',
                        columns: ':not(.no-export)'
                    }
                ],
                columnDefs: [
                    {
                      targets: [6, 7, 5], // Specify the column indexes to exclude
                      searchable: false,
                      export: false
                    }
                ]
            });
            table.buttons().container().appendTo('#example_wrapper .col-md-6:eq(0)');
        });
    }
            //  ================================================== //
            //     filter by date
            // ================================================== //



            // $('.filter-toggle').on('click', function () {
            //     $('.filter-content').toggle();
            // });

            // $('#filterButton').on('click', function () {
            //     var startDate = $('#startDateInput').val();
            //     var endDate = $('#endDateInput').val();
            //     var formattedStartDate = formatDate(startDate);
            //     var formattedEndDate = formatDate(endDate);
            
            //     table.columns(2).search(formattedStartDate + ' to ' + formattedEndDate).draw();
            // });
            
            // function formatDate(date) {
            //     var formattedDate = moment(date, 'MMM. DD, YYYY, h:mm a').format('YYYY-MM-DD');
            //     return formattedDate;
            // }

            // ================================================== //
            //     end filter by date
            // ================================================== //






    if ($("#example2").length) {

        $(document).ready(function () {
            $(document).ready(function () {
                var groupColumn = 2;
                var table = $('#example2').DataTable({
                    "columnDefs": [
                        { "visible": false, "targets": groupColumn }
                    ],
                    "order": [
                        [groupColumn, 'asc']
                    ],
                    "displayLength": 25,
                    "drawCallback": function (settings) {
                        var api = this.api();
                        var rows = api.rows({ page: 'current' }).nodes();
                        var last = null;

                        api.column(groupColumn, { page: 'current' }).data().each(function (group, i) {
                            if (last !== group) {
                                $(rows).eq(i).before(
                                    '<tr class="group"><td colspan="5">' + group + '</td></tr>'
                                );

                                last = group;
                            }
                        });
                    }
                });

                // Order by the grouping
                $('#example2 tbody').on('click', 'tr.group', function () {
                    var currentOrder = table.order()[0];
                    if (currentOrder[0] === groupColumn && currentOrder[1] === 'asc') {
                        table.order([groupColumn, 'desc']).draw();
                    } else {
                        table.order([groupColumn, 'asc']).draw();
                    }
                });
            });
        });
    }

    if ($("#example3").length) {

        $('#example3').DataTable({
            select: {
                style: 'multi'
            }
        });

    }
    if ($("#example4").length) {

        $(document).ready(function () {
            var table = $('#example4').DataTable({
                fixedHeader: true
            });
        });
    }

});