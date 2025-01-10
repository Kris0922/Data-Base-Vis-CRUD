
document.addEventListener('DOMContentLoaded', () => {
    const tableSelect = document.getElementById('tableSelect');
    const headerRow = document.getElementById('headerRow');
    const tableBody = document.getElementById('tableBody');
    const addRecordBtn = document.getElementById('addRecordBtn');
    const addRecordModal = document.getElementById('addRecordModal');
    const closeModalBtn = addRecordModal.querySelector('.close');
    const formFields = document.getElementById('formFields');
    const addRecordForm = document.getElementById('addRecordForm');

    const querySelect = document.getElementById('querySelect');
    const runQueryBtn = document.getElementById('runQueryBtn');
    const queryParamInput = document.getElementById('queryParam');

    const API_BASE_URL = 'http://localhost:5000/api';

    // Open modal to add a new record
    addRecordBtn.addEventListener('click', async () => {
        selectedTable = tableSelect.value;
        if (!selectedTable) {
            alert('Please select a table first.');
            return;
        }

        // Fetch the structure of the selected table to dynamically create form fields
        try {
            const response = await fetch(`${API_BASE_URL}/table/${selectedTable}`);
            const data = await response.json();

            if (data.columns) {
                formFields.innerHTML = ''; // Clear previous fields
                data.columns.forEach(column => {
                    // Skip the primary key column (e.g., id)
                    if (column === 'Model_ID') return;

                    const fieldDiv = document.createElement('div');
                    fieldDiv.className = 'form-field';
                    fieldDiv.innerHTML = `
                        <label>${column}:</label>
                        <input type="text" name="${column}" />
                    `;
                    formFields.appendChild(fieldDiv);
                });

                addRecordModal.style.display = 'block'; // Show the modal
            }
        } catch (error) {
            console.error('Error fetching table structure:', error);
            alert('Could not fetch table structure.');
        }
    });


    // Close modal
    closeModalBtn.addEventListener('click', () => {
        addRecordModal.style.display = 'none';
    });

    addRecordForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData(addRecordForm);
        const recordData = {};

        // Convert form data to JSON
        formData.forEach((value, key) => {
            recordData[key] = value;
        });

        try {
            const response = await fetch(`${API_BASE_URL}/table/${selectedTable}/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(recordData)
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                addRecordModal.style.display = 'none';
                loadTableData(selectedTable); // Reload table data
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error adding record:', error);
            alert('Failed to add record. Please check the backend.');
        }
    });


    // Close modal when clicking outside it
    window.addEventListener('click', (e) => {
        if (e.target === addRecordModal) {
            addRecordModal.style.display = 'none';
        }
    });
    async function loadTables() {
        try {
            const response = await fetch(`${API_BASE_URL}/tables`);
            const data = await response.json();

            if (data.tables) {
                data.tables.forEach(table => {
                    const option = document.createElement('option');
                    option.value = table;
                    option.textContent = table;
                    tableSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading tables:', error);
            alert('Error at loading tables. Check Backed');
        }
    }

    async function loadTableData(tableName) {
        try {
            headerRow.innerHTML = '<th>Loading...</th>';
            tableBody.innerHTML = '';

            const response = await fetch(`${API_BASE_URL}/table/${tableName}`);
            const data = await response.json();

            if (data.columns && data.data) {
                // Add columns including the Delete button
                headerRow.innerHTML = '';
                data.columns.forEach(column => {
                    const th = document.createElement('th');
                    th.textContent = column;
                    headerRow.appendChild(th);
                });
                const deleteHeader = document.createElement('th');
                deleteHeader.textContent = 'Actions';
                headerRow.appendChild(deleteHeader);

                // Populate table rows
                tableBody.innerHTML = '';
                data.data.forEach(row => {
                    const tr = document.createElement('tr');

                    // Populate columns
                    data.columns.forEach(column => {
                        const td = document.createElement('td');
                        td.textContent = row[column] ?? 'N/A';
                        tr.appendChild(td);
                    });

                    // Add Delete button
                    const deleteTd = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.className = 'action-button delete-button';
                    deleteButton.dataset.primaryKey = data.columns[0]; // Assume the first column is the primary key
                    deleteButton.dataset.value = row[data.columns[0]];
                    deleteButton.addEventListener('click', () => {
                        deleteRecord(tableName, deleteButton.dataset.primaryKey, deleteButton.dataset.value);
                    });
                    deleteTd.appendChild(deleteButton);
                    tr.appendChild(deleteTd);

                    tableBody.appendChild(tr);
                });
            }
        } catch (error) {
            console.error('Error loading table data:', error);
            headerRow.innerHTML = '<th>Error loading data</th>';
            alert('Error loading table data. Check backend.');
        }
    }

    async function deleteRecord(tableName, primaryKey, value) {
        if (!confirm(`Are you sure you want to delete the record with ${primaryKey} = ${value}?`)) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/table/${tableName}/delete`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ primary_key: primaryKey, value: value })
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                loadTableData(tableName); // Reload table data
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error deleting record:', error);
            alert('Failed to delete record. Please check the backend.');
        }
    }

    tableSelect.addEventListener('change', (e) => {
        const selectedTable = e.target.value;
        if (selectedTable) {
            loadTableData(selectedTable);
        } else {
            headerRow.innerHTML = '';
            tableBody.innerHTML = '';
        }
    });

    //////////////////////////
    // Load available queries into the select dropdown
    function loadQueries() {
        const queries = {
            simple: [
                { id: '1', label: 'Modele, mentori si competitii' },
                { id: '2', label: 'Modele si competitii dupa competitie (cu parametru)' },
                { id: '3', label: 'Jurati si competitii' },
                { id: '4', label: 'Mentori, modele si contracte' },
                { id: '5', label: 'Modele si detalii despre competitii' },
                { id: '6', label: 'Mentori fara modele asociate si competitii' }
            ],
            complex: [
                { id: '1', label: 'Modele cu mentori in competitii' },
                { id: '2', label: 'Jurati implicati dupa un anumit an (parametru)' },
                { id: '3', label: 'Modele implicate in competitii multiple' },
                { id: '4', label: 'Competitii populare cu modele multiple' },
            ]
        };

        for (const category in queries) {
            const optGroup = document.createElement('optgroup');
            optGroup.label = category === 'simple' ? 'Interogari simple' : 'Interogari complexe';

            queries[category].forEach(query => {
                const option = document.createElement('option');
                option.value = `${category}_${query.id}`;
                option.textContent = query.label;
                optGroup.appendChild(option);
            });

            querySelect.appendChild(optGroup);
        }
    }

    // Run selected query
    async function runQuery() {
        const selectedQuery = querySelect.value;
        const queryParam = queryParamInput.value;

        if (!selectedQuery) {
            alert('Please select a query to run.');
            return;
        }

        const [category, queryId] = selectedQuery.split('_');
        const endpoint = category === 'simple' ? 'simple_query' : 'complex_query';

        try {
            const url = `${API_BASE_URL}/${endpoint}/${queryId}?param=${encodeURIComponent(queryParam)}`;
            const response = await fetch(url);
            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Error running query:', error);
            alert('Failed to run query. Please check the backend.');
        }
    }

    // Display results in the table
    function displayResults(results) {
        const headerRow = document.getElementById('headerRow');
        const tableBody = document.getElementById('tableBody');

        if (!results || results.length === 0) {
            headerRow.innerHTML = '<th>No results</th>';
            tableBody.innerHTML = '';
            return;
        }

        // Populate table headers
        headerRow.innerHTML = '';
        const columns = Object.keys(results[0]);
        columns.forEach(column => {
            const th = document.createElement('th');
            th.textContent = column;
            headerRow.appendChild(th);
        });

        // Populate table rows
        tableBody.innerHTML = '';
        results.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(column => {
                const td = document.createElement('td');
                td.textContent = row[column] ?? 'N/A';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }

    // Event listeners
    runQueryBtn.addEventListener('click', runQuery);

    // Initialize the page
    loadQueries();
    ////////////////////////////

    loadTables();
});