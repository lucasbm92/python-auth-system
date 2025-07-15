import pymysql
from datetime import datetime

def migrate_database():
    """Add missing columns to the existing user table"""
    print("Starting database migration...")
    
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='lucasbm92',
            password='lbm291292',
            database='auth_system_db',
            connect_timeout=5
        )
        
        print("✅ Connected to database")
        
        cursor = connection.cursor()
        
        # Check current table structure
        cursor.execute("DESCRIBE user;")
        columns = cursor.fetchall()
        existing_columns = [col[0] for col in columns]
        
        print(f"Current columns: {existing_columns}")
        
        # Add missing columns
        migrations = []
        
        if 'email' not in existing_columns:
            migrations.append("ALTER TABLE user ADD COLUMN email VARCHAR(150) UNIQUE")
            print("- Will add email column")
        
        if 'reset_token' not in existing_columns:
            migrations.append("ALTER TABLE user ADD COLUMN reset_token VARCHAR(100) NULL")
            print("- Will add reset_token column")
        
        if 'reset_token_expiry' not in existing_columns:
            migrations.append("ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME NULL")
            print("- Will add reset_token_expiry column")
        
        if 'created_at' not in existing_columns:
            migrations.append("ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            print("- Will add created_at column")
        
        if not migrations:
            print("✅ No migrations needed - table is up to date")
            return
        
        # Execute migrations
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✅ Executed: {migration}")
            except Exception as e:
                print(f"❌ Error executing {migration}: {e}")
        
        connection.commit()
        print("✅ Database migration completed successfully!")
        
        # Show final table structure
        cursor.execute("DESCRIBE user;")
        columns = cursor.fetchall()
        print("\nFinal table structure:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate_database()
