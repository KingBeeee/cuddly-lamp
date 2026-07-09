// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FlareTrust {
    address public teeAddress;

    // Mapping to store wallet addresses and their verified credit scores
    mapping(address => uint256) public creditScores;

    // Events that our Python listener will catch
    event ScoreRequested(address indexed user);
    event ScoreUpdated(address indexed user, uint256 score);

    constructor() {
        // Set the deployer as the initial authorized TEE account
        teeAddress = msg.sender;
    }

    // Called by a user wanting to trigger a private credit score calculation
    function requestCreditScore() external {
        emit ScoreRequested(msg.sender);
    }

    // Called only by your Python TEE backend to save the score on-chain
    function submitCreditScore(address _user, uint256 _score) external {
        require(msg.sender == teeAddress, "Only the authorized TEE can submit scores");
        require(_score <= 1000, "Invalid score range");
        
        creditScores[_user] = _score;
        emit ScoreUpdated(_user, _score);
    }
}
