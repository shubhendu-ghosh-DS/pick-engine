import joblib

# Appliance-wise configuration
APPLIANCE_CONFIG = {
    'ac': {
        'model_path': 'models/ac_knn_model.pkl',
        'encoder_path': 'models/ac_encoders.pkl',
        'features_path': 'models/ac_features.pkl',
        'feature_order': ['ratings', 'actual_price', 'brand', 'power', 'star', 'inverter'],
    },
    'tv': {
        'model_path': 'models/tv_knn_model.pkl',
        'encoder_path': 'models/tv_encoders.pkl',
        'features_path': 'models/tv_features.pkl',
        'feature_order': ['ratings', 'actual_price', 'brand', 'length', 'LED', 'smart', 'ultra_hd'],
    },
    'fridge': {
        'model_path': 'models/fridge_knn_model.pkl',
        'encoder_path': 'models/fridge_encoders.pkl',
        'features_path': 'models/fridge_features.pkl',
        'feature_order': ['ratings', 'actual_price', 'brand', 'capacity', 'energy_star', 'door', 'cooling_tech'],
    },
    'wash': {
        'model_path': 'models/wash_knn_model.pkl',
        'encoder_path': 'models/wash_encoders.pkl',
        'features_path': 'models/wash_features.pkl',
        'feature_order': ['ratings', 'actual_price', 'brand', 'weight', 'load', 'energy_star'],
    }
}

# Load everything at startup
loaded_models = {}
for appliance, config in APPLIANCE_CONFIG.items():
    loaded_models[appliance] = {
        'model': joblib.load(config['model_path']),
        'encoders': joblib.load(config['encoder_path']),
        'features': joblib.load(config['features_path']),
    }






def recommend_product(input_dict, appliance):
    model = loaded_models[appliance]['model']
    encoders = loaded_models[appliance]['encoders']
    train_features = loaded_models[appliance]['features']

    # Preprocess input
    #processed = preprocess_single_product(input_dict, appliance, encoders)

    # Create input vector for KNN model based on feature order
    feature_order = {
        "ac": ['ratings', 'actual_price', 'brand', 'power', 'star', 'inverter'],
        "tv": ['ratings', 'actual_price', 'brand', 'length', 'LED', 'smart', 'ultra_hd'],
        "fridge": ['ratings', 'actual_price', 'brand', 'capacity', 'energy_star', 'door', 'cooling_tech'],
        "wash": ['ratings', 'actual_price', 'brand', 'weight', 'load', 'energy_star']
    }

    feature_vector = [input_dict.get(key, 0.0) for key in feature_order[appliance]]

    # Predict
    distances, indices = model.kneighbors([feature_vector], n_neighbors=6)
    
    recommendations = train_features.iloc[indices[0][1:]].copy()

    return recommendations


def preprocess_single_product(input_dict: dict, appliance: str) -> dict:
    processed = input_dict.copy()


    # Appliance-specific label encoding
    appliance_encoding_cols = {
        "ac": ['brand', 'power', 'star', 'inverter'],
        "tv": ['brand'],
        "fridge": ['brand', 'door', 'cooling_tech'],
        "wash": ['brand', 'load']
    }

    model_data = loaded_models[appliance]
    label_encoders = model_data['encoders']

    encoding_cols = appliance_encoding_cols.get(appliance.lower(), [])
    for col in encoding_cols:
        value = processed.get(col)
        if value is not None:
            le = label_encoders.get(col)
            if le:
                try:
                    processed[col] = int(le.transform([str(value)])[0])
                except ValueError:
                    # If unseen label, fallback to 0 or similar safe default
                    processed[col] = 0
            else:
                processed[col] = 0  # fallback if encoder is missing
        else:
            processed[col] = 0  # fallback if value is missing

    return processed