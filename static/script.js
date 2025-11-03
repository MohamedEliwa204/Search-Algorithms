
    // === Input Section ===
    const inputContainer = document.getElementById('input-container');
    const solveButton = document.getElementById('solve-button');
    const puzzleCells = document.querySelectorAll('.puzzle-cell');
    const algorithmSelect = document.getElementById('algorithm-select');
    const errorMessage = document.getElementById('error-message');
    const puzzleGrid = document.getElementById('puzzle-grid');

    // === Display Section ===
    const displayContainer = document.getElementById('display-container');
    const displayBoard = document.getElementById('display-board');
    const resetButton = document.getElementById('reset-button');
    const speedButton = document.getElementById('speed-button');

    // === Results Panel ===
    const resCost = document.getElementById('res-cost');
    const resDepth = document.getElementById('res-depth');
    const resNodes = document.getElementById('res-nodes');
    const resTime = document.getElementById('res-time');
    const resultsPanel = document.getElementById('results-panel'); 

    // === State ===
    let currentBoardState = []; 
    let animationTimer = null; 
    
    // === Animation Speed Settings ===
    const speedSettings = [
        { duration: 500, label: 'Speed: 1x' },  
        { duration: 200, label: 'Speed: 2.5x' }, 
        { duration: 100, label: 'Speed: 5x' }   
    ];
    let currentSpeedIndex = 0;
    let animationSpeed = speedSettings[currentSpeedIndex].duration; 

    // Speed button
    speedButton.textContent = speedSettings[currentSpeedIndex].label; 
    speedButton.style.marginTop = '10px'; 
    speedButton.style.width = '100%'; 


    // === Event Listeners ===
    solveButton.addEventListener('click', handleSubmit);
    resetButton.addEventListener('click', resetView);
    speedButton.addEventListener('click', toggleSpeed);
    puzzleCells.forEach(cell => cell.addEventListener('input', handleCellInput));
    
    

    function getBoardDimensions() {
        const boardWidth = displayBoard.clientWidth;
        const gapSize = boardWidth * 0.02; 
        const tileSize = (boardWidth - (2 * gapSize)) / 3;
        displayBoard.style.padding = `${gapSize}px`;
        return { tileSize, gapSize };
    }
    function validateDuplicates() {
        const values = {};
        let hasDuplicates = false;
        puzzleCells.forEach(cell => {
            const val = cell.value;
            if (val !== "") values[val] = (values[val] || 0) + 1;
        });
        puzzleCells.forEach(cell => {
            const val = cell.value;
            if (val !== "" && values[val] > 1) {
                cell.classList.add('invalid');
                hasDuplicates = true;
            } else {
                cell.classList.remove('invalid');
            }
        });
        if (!hasDuplicates && errorMessage.textContent.includes("duplicate")) {
            errorMessage.classList.remove('show');
        }
        return hasDuplicates;
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add('show');
        if (!message.includes("duplicate")) {
            puzzleGrid.classList.add('shake');
            setTimeout(() => puzzleGrid.classList.remove('shake'), 500);
        }
    }
    async function handleSubmit() {
        errorMessage.classList.remove('show');
        const hasDuplicates = validateDuplicates() ;
        if(hasDuplicates){
            showError("Board must not contain duplicate numbers.");
            return;
        }
        let board = [];
        let  isValid = true ;
        puzzleCells.forEach(cell => {
            const val = cell.value ;
            if (val === "" || isNaN(val)) isValid = false;
            board.push(parseInt(val, 10));
        })
            if (!isValid) {
            showError("Please fill all cells with numbers.");
            return;
        }


        const algorithm = algorithmSelect.value;
        const dataToSend = { initial_state: board, algorithm };


        solveButton.disabled = true ;
        solveButton.textContent = "Solving....."
        try{
            const response = await fetch('/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend),
            });
            const result = await response.json();
            if(!response.ok) throw new Error(result.error);

            displayContainer.style.display = 'block';
            window.scrollTo(200,1000);
            showSolution(result, board);
        }
        catch(error){
            showError(`Connection to server failed: ${error.message}`);
            solveButton.disabled = false ;
            solveButton.textContent = "Solve"
        }
        
    }
    function showSolution(result,initialState){
        resCost.textContent = result.cost;
        resDepth.textContent = result.search_depth;
        resNodes.textContent = result.nodes_expanded;
        resTime.textContent = parseFloat(result.time_taken).toFixed(4);

        currentBoardState = [...initialState];
        initDisplayBoard(initialState);

        animationTimer = setTimeout(() => {
            animateSolution(result.path);
        }, animationSpeed);
    }
    function initDisplayBoard(initialState){
        displayBoard.innerHTML = '';
        const {tileSize,gapSize} = getBoardDimensions();
        for (let i = 0 ; i< initialState.length ; i++ ){
            const val = initialState[i];
            const tile = document.createElement('div');
            tile.classList.add('display-tile');
            tile.setAttribute('data-value',val);
            if(val === 0 ) tile.classList.add('empty');
            else tile.textContent = val ;

            const { row, col } = getRowCol(i);
            tile.style.top = `${row * (tileSize + gapSize)}px`;
            tile.style.left = `${col * (tileSize + gapSize)}px`;
            tile.style.height = `${tileSize}px` ;
            tile.style.width = `${tileSize}px` ;
            tile.style.fontSize = `${tileSize * 0.4}px`;
            tile.style.transition = `all ${animationSpeed / 1000}s ease-in-out`;
            displayBoard.appendChild(tile);
        }
    }
    function getRowCol(i){
        return {row: Math.floor(i/3) ,col: i % 3 } ;
    }
    function applyMove(move){
        const {tileSize,gapSize} = getBoardDimensions();
        const zeroIndex = currentBoardState.indexOf(0);
        const zeroCol = zeroIndex%3;
        const zeroRow = Math.floor(zeroIndex/3);
        let target = -1 ;
        if (move === "Up" && zeroRow > 0 ) target = zeroIndex - 3 ;
        else if (move === "Down" && zeroRow < 2) target = zeroIndex + 3 ;
        else if (move === "Right" && zeroCol < 2 ) target = zeroIndex +1 ;
        else if (move === "Left" && zeroCol > 0 ) target = zeroIndex -1 ;
        if (target < 0 || target > 8 )return ;
        
        const targetValue = currentBoardState[target];
        const zeroTile = document.querySelector('.display-tile[data-value="0"]');
        const targetTile = document.querySelector(`.display-tile[data-value="${targetValue}"]`);

        let targetCol = target%3;
        let targetRow = Math.floor(target/3);

        zeroTile.style.left = `${targetCol * (tileSize + gapSize)}px`;
        zeroTile.style.top = `${targetRow * (tileSize + gapSize)}px`;
        targetTile.style.left = `${zeroCol * (tileSize + gapSize)}px`;
        targetTile.style.top = `${zeroRow * (tileSize + gapSize)}px`;

        currentBoardState[zeroIndex] = targetValue ;
        currentBoardState[target]  = 0 ;
    }
    function animateSolution(path) {
        if (path.length === 0) return;
        const move = path.shift(); 
        applyMove(move);
        if (path.length > 0) {
            animationTimer = setTimeout(() => animateSolution(path), animationSpeed); 
        }
    }
    function toggleSpeed() {
        console.log("+")
        currentSpeedIndex = (currentSpeedIndex + 1) % speedSettings.length;
        animationSpeed = speedSettings[currentSpeedIndex].duration;
        speedButton.textContent = speedSettings[currentSpeedIndex].label;
        document.querySelectorAll('.display-tile').forEach(tile => {
            tile.style.transition = `all ${animationSpeed / 1000}s ease-in-out`;
        });
    }
    function handleCellInput(e) {
        const value = e.target.value.replace(/[^0-9]/g, '');
        if (value === "" || parseInt(value, 10) < 0 || parseInt(value, 10) > 8) {
            e.target.value = "";
        } else {
            e.target.value = value;
        }
        validateDuplicates();
    }

    // === Reset View ===
    function resetView() {

        if (animationTimer) {
            clearTimeout(animationTimer);
            animationTimer = null;
        }
        solveButton.disabled = false;
        solveButton.textContent = "Solve";
        errorMessage.classList.remove('show');
        currentBoardState = [];
        currentSpeedIndex = 0;
        animationSpeed = speedSettings[currentSpeedIndex].duration;
        speedButton.textContent = speedSettings[currentSpeedIndex].label;
        displayContainer.style.display = 'none';
    }