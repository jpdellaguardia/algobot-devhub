import pandas as pd
import os
from glob import glob

# Caminhos relativos
RAW_DIR = os.path.join("..", "..", "data", "raw")
PROCESSED_DIR = os.path.join("..", "..", "data", "processed")

# Cria pasta processed se não existir
os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_data(df):
    """Limpa os dados removendo nulls e duplicados"""
    # Remove valores nulos
    df_clean = df.dropna()
    
    # Remove duplicados baseado no timestamp
    df_clean = df_clean.drop_duplicates(subset=['open_time'])
    
    # Converte colunas numéricas
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Ordena por timestamp
    df_clean = df_clean.sort_values('open_time').reset_index(drop=True)
    
    return df_clean

# Processa todos os arquivos CSV da pasta raw
csv_files = glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    print("❌ Nenhum arquivo CSV encontrado na pasta raw")
else:
    print(f"📁 Encontrados {len(csv_files)} arquivos para processar")
    
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        print(f"🔄 Processando {filename}...")
        
        # Carrega dados
        df = pd.read_csv(file_path)
        original_rows = len(df)
        
        # Limpa dados
        df_clean = clean_data(df)
        clean_rows = len(df_clean)
        
        # Salva arquivo processado
        processed_path = os.path.join(PROCESSED_DIR, filename)
        df_clean.to_csv(processed_path, index=False)
        
        # Remove arquivo raw após processamento
        os.remove(file_path)
        
        removed_rows = original_rows - clean_rows
        print(f"✅ {filename} processado: {original_rows} → {clean_rows} linhas (-{removed_rows}) | Raw removido")
    
    print(f"🎉 Processamento concluído! Arquivos salvos em: {PROCESSED_DIR}")