const { DataTypes } = require('sequelize');
const sequelize = require('../config');

const User = sequelize.define('User', {
  user_id: {
    type: DataTypes.STRING,
    unique: true,
    allowNull: false
  },
  user_password: {
    type: DataTypes.STRING,
    allowNull: false
  }}, 
  
  { tableName: 'users', 
    timestamps: false
  }

);

module.exports = User;
