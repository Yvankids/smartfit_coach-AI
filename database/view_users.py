import mariadb
from config.db_config import DB_CONFIG
from tabulate import tabulate

def view_users():
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.user_id, u.username, u.email, u.created_at, u.last_login,
                   p.full_name, p.age, p.weight, p.height, p.fitness_goal
            FROM users u
            LEFT JOIN user_profiles p ON u.user_id = p.user_id
        """)
        
        users = cursor.fetchall()
        headers = ['ID', 'Username', 'Email', 'Created', 'Last Login', 
                  'Full Name', 'Age', 'Weight', 'Height', 'Fitness Goal']
        
        if users:
            print("\n=== SmartFit Coach Users ===\n")
            print(tabulate(users, headers=headers, tablefmt='grid'))
            print(f"\nTotal users: {len(users)}")
        else:
            print("No users found in the database.")
            
    except mariadb.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_users()