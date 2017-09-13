
# coding: utf-8

# Import Files

# In[1]:

import sqlite3
from datetime import datetime


# Define database name

# In[2]:

dbname = 'Bid_Ask.db'


# Create database

# In[3]:

def create_db():
    conn = sqlite3.connect(dbname)
    conn.close()


# Create bid and ask table

# In[4]:

def create_table():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS bid
                (ID INTEGER, 
                Exchange TEXT,
                Symbol TEXT,  
                Bid REAL, 
                BidVolume REAL,
                TimeStamp INTEGER,
                TickTime REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS ask
                (ID INTEGER, 
                Exchange TEXT,
                Symbol TEXT, 
                Ask REAL,
                AskVolume REAL,
                TimeStamp INTEGER,
                TickTime REAL)''')    
        
    c.close()
    conn.close()


# Increased ID

# In[ ]:

def increase_id(c, exchange, symbol):
    c.execute('''SELECT MAX(ID) FROM bid WHERE Symbol = ? AND Exchange = ?'''
                    , (symbol, exchange))
    max_tick = c.fetchone()[0]

    if max_tick == None:
        max_tick = 1
    else:
        max_tick += 1

    return max_tick


# Return True if tick change

# In[ ]:

def is_tick_change(c, exchange, symbol, orderbook):
    is_bid = False
    is_ask = False
    
    c.execute('''SELECT MAX(ID) FROM bid WHERE Symbol = ? AND Exchange = ?;'''
                    , (symbol, exchange))
    max_tick_bid = c.fetchone()[0]
    
    c.execute('''SELECT MAX(ID) FROM ask WHERE Symbol = ? AND Exchange = ?;'''
                    , (symbol, exchange))
    max_tick_ask = c.fetchone()[0]
    
    c.execute('''SELECT Bid FROM  bid WHERE Exchange = ? AND ID = ? AND Symbol = ?;'''
                  , (exchange, max_tick_bid, symbol))
    previous_bid = c.fetchall()
    
    c.execute('''SELECT Ask FROM ask WHERE Exchange = ? AND ID = ? AND Symbol = ?;'''
                  , (exchange, max_tick_ask, symbol))
    previous_ask = c.fetchall()

    if len(previous_bid) > 0 and len(previous_ask) > 0:
        if previous_bid[0][0] != orderbook['bids'][0]: 
            is_bid = True
        
        if previous_ask[0][0] != orderbook['asks'][0]:
            is_ask = True
        
        return is_bid, is_ask
        
    else:
        return True, True


# Insert price data into database

# In[ ]:

def insert_data(orderbook, exchange, symbol, time_tick_change):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    is_insert = True

    increased_id = increase_id(c, exchange, symbol)
    
    is_bid, is_ask = is_tick_change(c, exchange, symbol, orderbook)

    if is_bid or is_ask:
        time = 0
        if (is_bid):
            time = time_tick_change

        c.execute('''INSERT INTO bid
                            (ID, Exchange, Symbol, Bid, BidVolume, TimeStamp, TickTime) 
                     VALUES
                            (?, ?, ?, ?, ?, ?, ?)''',
                  (increased_id, exchange, symbol, orderbook['bids'][0][0], orderbook['bids'][0][1], orderbook['timestamp'], time))

        time = 0
        if(is_ask):
            time = time_tick_change

        c.execute('''INSERT INTO ask
                            (ID, Exchange, Symbol, Ask, AskVolume, TimeStamp, TickTime) 
                     VALUES
                            (?, ?, ?, ?, ?, ?, ?)''',
                  (increased_id, exchange, symbol, orderbook['asks'][0][0], orderbook['asks'][0][1], orderbook['timestamp'], time))

        conn.commit()
        is_insert = True

    c.close()
    conn.close()
    return is_insert
