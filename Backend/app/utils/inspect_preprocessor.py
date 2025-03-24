import pickle
import os

def inspect_preprocessor():
    try:
        
        preprocessor_path = "preprocessor.pkl"
        print(f"Loading preprocessor from: {preprocessor_path}")
        
        # Use custom unpickler to handle module name changes
        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if module == "preprocessing":
                    module = "data_preprocessing"
                return super().find_class(module, name)
        
        with open(preprocessor_path, "rb") as f:
            preprocessor = CustomUnpickler(f).load()
        
        print("\nPreprocessor Information:")
        print("------------------------")
        
        # Print feature names used during fit
        if hasattr(preprocessor, 'feature_names_'):
            print("\nFeature names used during fit:")
            print(preprocessor.feature_names_)
        else:
            print("\nNo feature_names_ attribute found")
            
        # Print column transformer feature names if available
        if hasattr(preprocessor, 'get_feature_names_out'):
            print("\nFeature names after transformation:")
            print(preprocessor.get_feature_names_out())
        else:
            print("\nNo get_feature_names_out method available")
            
        # Print the structure of the preprocessor
        print("\nPreprocessor structure:")
        if hasattr(preprocessor, 'named_transformers_'):
            for name, transformer in preprocessor.named_transformers_.items():
                print(f"\nTransformer: {name}")
                print(f"Type: {type(transformer)}")
                if hasattr(transformer, 'get_feature_names_out'):
                    print("Features produced:")
                    print(transformer.get_feature_names_out())
                    
    except Exception as e:
        print(f"Error inspecting preprocessor: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    inspect_preprocessor() 