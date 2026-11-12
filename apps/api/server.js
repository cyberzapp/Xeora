const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { createClient } = require('@supabase/supabase-js');
const { Queue } = require('bullmq');

dotenv.config();

const app = express();
const port = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

// Initialize Supabase Client
const supabaseUrl = process.env.SUPABASE_URL || 'http://localhost:54321';
const supabaseKey = process.env.SUPABASE_ANON_KEY || 'your-anon-key';
const supabase = createClient(supabaseUrl, supabaseKey);

// Initialize BullMQ Queue
const connection = {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379', 10),
};
const taskQueue = new Queue('xeora-tasks', { connection });

// Heuristics Engine
function calculatePriority(title, description) {
    const text = `${title} ${description}`.toLowerCase();
    let priority = 10; // Default priority (lower number = higher priority in BullMQ)
    
    if (text.includes('critical') || text.includes('down') || text.includes('outage') || text.includes('urgent')) {
        priority = 1;
    } else if (text.includes('high') || text.includes('error') || text.includes('fail')) {
        priority = 3;
    } else if (text.includes('medium') || text.includes('warning')) {
        priority = 5;
    }
    return priority;
}

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'xeora-api' });
});

// Endpoint to ingest a task
app.post('/api/tasks', async (req, res) => {
    const { title, description } = req.body;
    
    if (!title || !description) {
        return res.status(400).json({ error: 'Title and description are required' });
    }
    
    // 1. Calculate Priority using Heuristics Engine
    const priority = calculatePriority(title, description);

    // 2. Insert task into Supabase (status: queued)
    const { data: task, error } = await supabase
        .from('tasks')
        .insert([{ title, description, status: 'queued' }])
        .select()
        .single();
        
    if (error) {
        console.error('Error inserting task:', error);
        return res.status(500).json({ error: error.message });
    }
    
    // 3. Add to BullMQ with calculated priority
    try {
        await taskQueue.add('process-task', { taskId: task.id, title, description }, { priority });
        console.log(`Task ${task.id} queued with priority ${priority}`);
    } catch (err) {
        console.error('Failed to add task to queue:', err);
        return res.status(500).json({ error: 'Failed to queue task' });
    }

    res.json({ message: 'Task queued successfully', task, priority });
});

app.listen(port, () => {
    console.log(`Xeora Node API listening on port ${port}`);
});
