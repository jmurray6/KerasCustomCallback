

def write_training_metrics(
        cursor, 
        model_name, 
        model_type, 
        model_pkg, 
        duration,
        epochs, 
        lr, 
        accuracy, 
        loss, 
        accuracy_list, 
        loss_list):
    cursor.execute("""
        INSERT INTO MODELS (
        model_name, 
        model_type, 
        model_pkg
        ) VALUES (%s, %s, %s)
        ON CONFLICT (model_name) DO UPDATE SET model_name=EXCLUDED.model_name
        RETURNING model_id
        """, (model_name, model_type, model_pkg))
    
    model_id = cursor.fetchone()[0]

    cursor.execute(f"""
        INSERT INTO TRAINING (
        model_id, 
        training_duration,
        epochs,
        learning_rate,
        accuracy,
        loss,
        accuracy_list,
        loss_list
        ) VALUES (
        {model_id},
        {duration},
        {epochs},
        {lr},
        {accuracy},
        {loss},
        %s,
        %s
        )
        """,
        (accuracy_list,loss_list)
        )


    
