-- Production Database Migration Script
-- Adds the highest_score column to the userprogress table

-- Check if column exists and add it if it doesn't
DO $$ 
BEGIN
    -- Add the highest_score column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'userprogress' 
        AND column_name = 'highest_score'
    ) THEN
        ALTER TABLE userprogress ADD COLUMN highest_score INTEGER DEFAULT 0;
        
        -- Update existing records to set highest_score = score
        UPDATE userprogress SET highest_score = score WHERE highest_score = 0;
        
        RAISE NOTICE 'Successfully added highest_score column to userprogress table';
    ELSE
        RAISE NOTICE 'highest_score column already exists in userprogress table';
    END IF;
END $$;
