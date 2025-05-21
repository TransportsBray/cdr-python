-- sql/initialize_3cx_db.sql

CREATE TABLE IF NOT EXISTS cdr_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    call_id VARCHAR(100) NOT NULL,
    caller VARCHAR(50),
    callee VARCHAR(50),
    call_start DATETIME,
    call_end DATETIME,
    duration INT,
    call_type VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 