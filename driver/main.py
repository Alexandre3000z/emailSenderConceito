from driver.chrome import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import json
from typing import Dict, List
from datetime import datetime

class ExtratorPorTexto:
    """Classe para extrair dados de contato usando apenas texto da página"""
    
    def __init__(self):
        self.padroes = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'telefone_br': r'(?:\+55|55)?\s*\(?\d{2}\)?\s*\d{4,5}[-\s]?\d{4}',
            'telefone_internacional': r'\+\d{1,3}\s*\(?\d{1,4}\)?\s*\d{4,10}',
            'stand': r'(?:F-|Booth|Estande|Stand)\s*[A-Z0-9-]+',
            'website': r'https?://[^\s<>"\'\)]+',
            'rede_social': r'(?:instagram\.com|facebook\.com|linkedin\.com|twitter\.com|youtube\.com|wa\.me)/[^\s<>"\']+',
        }
        
        self.palavras_chave = {
            'sobre': ['sobre', 'descrição', 'quem somos', 'empresa', 'história', 'sobre nós'],
            'contato': ['contato', 'fale conosco', 'email', 'telefone', 'whatsapp'],
            'equipe': ['equipe', 'time', 'colaboradores', 'funcionários', 'membros'],
            'produtos': ['produtos', 'serviços', 'soluções', 'catálogo', 'linha'],
            'redes': ['redes sociais', 'social media', 'siga-nos', 'instagram', 'facebook'],
            'localizacao': ['stand', 'estande', 'booth', 'local', 'pavilhão'],
        }
    
    def extrair_dados_completos(self, texto: str, url: str = "") -> Dict:
        """Extrai todos os dados do texto da página"""
        
        dados = {
            'url': url,
            'nome_empresa': self._extrair_nome_empresa(texto),
            'descricao': self._extrair_descricao(texto),
            'categoria': self._extrair_categoria(texto),
            'stand': self._extrair_stand(texto),
            'emails': self._extrair_emails(texto),
            'telefones': self._extrair_telefones(texto),
            'websites': self._extrair_websites(texto),
            'redes_sociais': self._extrair_redes_sociais(texto),
            'produtos_detectados': self._extrair_produtos(texto),
            'equipe_extraida': self._extrair_equipe(texto),
            'palavras_chave': self._detectar_palavras_chave(texto)
        }
        
        return dados
    
    def _extrair_nome_empresa(self, texto: str) -> str:
        """Extrai nome da empresa do texto"""
        linhas = [l.strip() for l in texto.split('\n') if l.strip()]
        
        # Primeira linha com mais de 3 caracteres que não parece título genérico
        for linha in linhas[:10]:
            if len(linha) > 3 and not self._is_generico(linha):
                if any(c.isupper() for c in linha[:3]) or len(linha.split()) >= 2:
                    return linha
        
        # Tentar encontrar padrão de empresa
        empresa_pattern = r'([A-Z][A-Z\s]+(?:LTDA|LTD|S/A|SA|INC|CORP|CO\.?|LLC|GMBH))|([A-Z][a-z]+\s+(?:Indústria|Comércio|Equipamentos|Biossegurança))'
        match = re.search(empresa_pattern, texto, re.IGNORECASE)
        if match:
            return match.group(0).strip()
        
        return ""
    
    def _is_generico(self, texto: str) -> bool:
        """Verifica se o texto é genérico"""
        genericos = ['sobre', 'descrição', 'contato', 'home', 'início', 'produtos', 
                    'serviços', 'empresa', 'parceiros', 'eventos', 'notícias', 'blog']
        return any(g in texto.lower() for g in genericos)
    
    def _extrair_descricao(self, texto: str) -> str:
        """Extrai a descrição da empresa"""
        paragrafos = [p.strip() for p in texto.split('\n') if len(p.strip()) > 50 and not re.search(r'@|https?://', p)]
        
        descricoes = []
        for p in paragrafos:
            if len(p) > 60 and not self._is_generico(p[:50]):
                if any(word in p.lower() for word in ['somos', 'empresa', 'fundada', 'líderes', 'soluções', 'qualidade', 'produção']):
                    descricoes.append(p)
        
        return ' '.join(descricoes[:3]) if descricoes else ""
    
    def _extrair_emails(self, texto: str) -> List[str]:
        """Extrai todos os emails do texto"""
        emails = re.findall(self.padroes['email'], texto)
        emails_validos = []
        for email in emails:
            if not any(exemplo in email.lower() for exemplo in ['exemplo', 'teste', 'fake', 'sample']):
                emails_validos.append(email.lower())
        return list(set(emails_validos))
    
    def _extrair_telefones(self, texto: str) -> List[str]:
        """Extrai todos os telefones do texto"""
        telefones = []
        
        padroes_telefone = [
            r'(?:\+55|55)?\s*\(?\d{2}\)?\s*\d{4,5}[-\s]?\d{4}',
            r'\+\d{1,3}\s*\(?\d{1,4}\)?\s*\d{4,10}',
            r'\(\d{2,3}\)\s*\d{4,5}-\d{4}',
            r'\d{4,5}[-.\s]\d{4}',
        ]
        
        for padrao in padroes_telefone:
            encontrados = re.findall(padrao, texto)
            telefones.extend([t.strip() for t in encontrados if len(t.strip()) > 8])
        
        telefones_limpos = []
        for tel in telefones:
            tel_limpo = re.sub(r'\s+', ' ', tel).strip()
            if len(tel_limpo) >= 10 and tel_limpo not in telefones_limpos:
                telefones_limpos.append(tel_limpo)
        
        return telefones_limpos
    
    def _extrair_websites(self, texto: str) -> List[str]:
        """Extrai todos os websites do texto"""
        urls = re.findall(r'https?://[^\s<>"\'\)]+', texto)
        
        websites = []
        for url in urls:
            url = re.sub(r'[.,;:!?)]+$', '', url)
            if url.startswith('http'):
                if not any(social in url.lower() for social in ['instagram', 'facebook', 'linkedin', 'twitter', 'youtube']):
                    websites.append(url)
        
        return list(set(websites))
    
    def _extrair_redes_sociais(self, texto: str) -> Dict[str, str]:
        """Extrai links de redes sociais"""
        redes = {
            'instagram': '',
            'facebook': '',
            'linkedin': '',
            'twitter': '',
            'youtube': '',
            'whatsapp': '',
        }
        
        padroes_redes = {
            'instagram': r'(?:https?://)?(?:www\.)?instagram\.com/[^\s<>"\']+',
            'facebook': r'(?:https?://)?(?:www\.)?facebook\.com/[^\s<>"\']+',
            'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/[^\s<>"\']+',
            'twitter': r'(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)/[^\s<>"\']+',
            'youtube': r'(?:https?://)?(?:www\.)?youtube\.com/[^\s<>"\']+',
            'whatsapp': r'(?:https?://)?(?:www\.)?wa\.me/[^\s<>"\']+|https?://api\.whatsapp\.com/send\?phone=\d+',
        }
        
        for rede, padrao in padroes_redes.items():
            match = re.search(padrao, texto)
            if match:
                url = match.group(0)
                if not url.startswith('http'):
                    url = 'https://' + url
                redes[rede] = url
        
        return redes
    
    def _extrair_stand(self, texto: str) -> str:
        """Extrai o número do stand"""
        matches = re.findall(self.padroes['stand'], texto, re.IGNORECASE)
        if matches:
            return matches[0].strip()
        
        padroes_alternativos = [
            r'Stand\s*[:#]\s*([A-Z0-9-]+)',
            r'Booth\s*[:#]\s*([A-Z0-9-]+)',
            r'Est[ãa]nd\s*[:#]\s*([A-Z0-9-]+)',
        ]
        
        for padrao in padroes_alternativos:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extrair_categoria(self, texto: str) -> str:
        """Extrai categoria/premium/badge"""
        padroes_categoria = [
            r'\b(Premium|Gold|Silver|Bronze|Platinum|Diamond|Ouro|Prata|Bronze)\b',
            r'Categoria\s*[:#]\s*([A-Za-z\s]+)',
            r'Nível\s*[:#]\s*([A-Za-z\s]+)',
        ]
        
        for padrao in padroes_categoria:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                return match.group(1 if '(' in padrao else 0).strip()
        
        return ""
    
    def _extrair_produtos(self, texto: str) -> List[str]:
        """Extrai nomes de produtos do texto"""
        produtos = []
        
        padroes_produto = [
            r'(?:Autoclave|Compressor|Incubadora|Seladora|Esterilizador|Equipamento)\s+[A-Za-z0-9\s]+(?:\d+(?:\s*[Ll]itros)?)',
            r'(?:Modelo|Série)\s+[A-Za-z0-9-]+',
        ]
        
        for padrao in padroes_produto:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            produtos.extend([m.strip() for m in matches if len(m.strip()) > 5])
        
        # Buscar por listas de produtos em bullet points
        bullets = re.findall(r'[•\-*]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', texto)
        for bullet in bullets:
            if len(bullet) > 10 and not any(p in bullet.lower() for p in ['sobre', 'contato', 'email']):
                produtos.append(bullet.strip())
        
        return list(set(produtos))[:10]  # Limitar a 10 produtos
    
    def _extrair_equipe(self, texto: str) -> List[Dict]:
        """Extrai membros da equipe do texto"""
        equipe = []
        
        # Padrão: Nome - Cargo ou Nome (Cargo)
        padroes_nome_cargo = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[-–]\s*([A-Za-z\s]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(([A-Za-z\s]+)\)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*:\s*([A-Za-z\s]+)',
        ]
        
        for padrao in padroes_nome_cargo:
            matches = re.findall(padrao, texto)
            for nome, cargo in matches:
                nome = nome.strip()
                cargo = cargo.strip()
                if len(nome) > 3 and len(cargo) > 2:
                    # Verificar se já não foi adicionado
                    if not any(m['nome'] == nome for m in equipe):
                        equipe.append({'nome': nome, 'cargo': cargo})
        
        # Também buscar por cargos conhecidos
        cargos_conhecidos = ['Vendedor', 'Gerente', 'Diretor', 'Assistente', 'Coordenador', 'Analista', 'Presidente', 'CEO', 'CTO', 'CFO']
        for cargo in cargos_conhecidos:
            padrao = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+{cargo}'
            matches = re.findall(padrao, texto)
            for nome in matches:
                nome = nome.strip()
                if len(nome) > 3:
                    if not any(m['nome'] == nome for m in equipe):
                        equipe.append({'nome': nome, 'cargo': cargo})
        
        return equipe[:15]  # Limitar a 15 membros
    
    def _detectar_palavras_chave(self, texto: str) -> List[str]:
        """Detecta palavras-chave no texto"""
        palavras_encontradas = []
        texto_lower = texto.lower()
        
        for chave, palavras in self.palavras_chave.items():
            if any(p in texto_lower for p in palavras):
                palavras_encontradas.append(chave)
        
        return list(set(palavras_encontradas))


def aceitar_cookies(driver):
    """Aceita os cookies se o banner aparecer"""
    try:
        aceitar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-hook="cookie-banner-accept-all-button"]')
            )
        )
        aceitar.click()
        print("✅ Cookies aceitos!")
        time.sleep(50)
        return True
    except:
        print("ℹ️ Banner de cookies não apareceu ou já foi aceito")
        return False


def extrair_dados_pagina(driver, url, extrator):
    """Extrai dados de uma página usando o extrator por texto"""
    try:
        # Aguardar carregamento da página
        time.sleep(3)
        
        # Pegar todo o texto da página
        texto_completo = driver.find_element(By.TAG_NAME, "body").text
        
        # Verificar se a página carregou corretamente
        if not texto_completo or len(texto_completo) < 50:
            return {'status': 'erro', 'motivo': 'Página vazia ou não carregou'}
        
        # Extrair dados usando o extrator
        dados = extrator.extrair_dados_completos(texto_completo, url)
        dados['status'] = 'sucesso'
        
        return dados
        
    except Exception as e:
        return {
            'status': 'erro',
            'motivo': str(e),
            'url': url
        }


def salvar_resultados(resultados, nome_arquivo="expositores_extraidos"):
    """Salva os resultados em Excel e JSON"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Converter para DataFrame
    df_resultados = pd.DataFrame(resultados)
    
    # Salvar em Excel
    arquivo_excel = f"{nome_arquivo}_{timestamp}.xlsx"
    with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
        # Dados principais
        df_resultados.to_excel(writer, sheet_name='Dados Principais', index=False)
        
        # Separar redes sociais em colunas
        if 'redes_sociais' in df_resultados.columns:
            redes_df = pd.json_normalize(df_resultados['redes_sociais'].fillna({}))
            redes_df.index = df_resultados.index
            redes_df.to_excel(writer, sheet_name='Redes Sociais', index=False)
        
        # Separar equipe em colunas
        if 'equipe_extraida' in df_resultados.columns:
            equipe_rows = []
            for idx, row in df_resultados.iterrows():
                equipe = row.get('equipe_extraida', [])
                if equipe:
                    for membro in equipe:
                        equipe_rows.append({
                            'url': row.get('url', ''),
                            'nome_empresa': row.get('nome_empresa', ''),
                            'membro_nome': membro.get('nome', ''),
                            'membro_cargo': membro.get('cargo', '')
                        })
            if equipe_rows:
                df_equipe = pd.DataFrame(equipe_rows)
                df_equipe.to_excel(writer, sheet_name='Equipe', index=False)
        
        # Separar produtos
        if 'produtos_detectados' in df_resultados.columns:
            produtos_rows = []
            for idx, row in df_resultados.iterrows():
                produtos = row.get('produtos_detectados', [])
                if produtos:
                    for produto in produtos:
                        produtos_rows.append({
                            'url': row.get('url', ''),
                            'nome_empresa': row.get('nome_empresa', ''),
                            'produto': produto
                        })
            if produtos_rows:
                df_produtos = pd.DataFrame(produtos_rows)
                df_produtos.to_excel(writer, sheet_name='Produtos', index=False)
    
    print(f"\n✅ Arquivo Excel salvo: {arquivo_excel}")
    
    # Salvar também em JSON (backup)
    arquivo_json = f"{nome_arquivo}_{timestamp}.json"
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo JSON salvo: {arquivo_json}")
    
    return arquivo_excel


if __name__ == "__main__":
    # Carregar dados dos expositores
    df = pd.read_excel("expositores.xlsx")
    
    # Inicializar driver e extrator
    driver = get_driver()
    extrator = ExtratorPorTexto()
    
    # Acessar primeira página para aceitar cookies
    print("\n🚀 Iniciando extração de dados...")
    driver.get(df.iloc[0]["Link"])
    aceitar_cookies(driver)
    
    # Lista para armazenar todos os resultados
    todos_resultados = []
    
    # Contadores para estatísticas
    total_sucesso = 0
    total_erro = 0
    
    # Processar cada expositor
    for index, row in df.iterrows():
        nome = row["Nome"]
        link = row["Link"]
        
        print(f"\n📌 [{index+1}/{len(df)}] Processando: {nome[:50]}...")
        
        try:
            # Acessar a página
            driver.get(link)
            
            # Extrair dados
            dados = extrair_dados_pagina(driver, link, extrator)
            
            if dados.get('status') == 'sucesso':
                total_sucesso += 1
                
                # Mostrar resumo dos dados encontrados
                print(f"  ✅ Empresa: {dados.get('nome_empresa', 'N/A')[:40]}")
                if dados.get('emails'):
                    print(f"  📧 Emails: {', '.join(dados['emails'])}")
                if dados.get('telefones'):
                    print(f"  📞 Telefones: {', '.join(dados['telefones'])}")
                if dados.get('websites'):
                    print(f"  🌐 Website: {dados['websites'][0]}")
                if dados.get('redes_sociais') and any(dados['redes_sociais'].values()):
                    redes_encontradas = [k for k, v in dados['redes_sociais'].items() if v]
                    print(f"  📱 Redes: {', '.join(redes_encontradas)}")
                if dados.get('produtos_detectados'):
                    print(f"  🏷️ Produtos: {len(dados['produtos_detectados'])} encontrados")
                if dados.get('equipe_extraida'):
                    print(f"  👥 Equipe: {len(dados['equipe_extraida'])} membros")
                    
                # Adicionar o nome original da planilha
                dados['nome_original_planilha'] = nome
                todos_resultados.append(dados)
                
            else:
                total_erro += 1
                print(f"  ❌ Erro: {dados.get('motivo', 'Desconhecido')}")
                todos_resultados.append({
                    'url': link,
                    'nome_original_planilha': nome,
                    'status': 'erro',
                    'motivo': dados.get('motivo', 'Erro desconhecido')
                })
            
            # Salvar checkpoint a cada 10 páginas
            if (index + 1) % 10 == 0:
                print(f"\n💾 Checkpoint: Salvando progresso ({index+1}/{len(df)})...")
                checkpoint_file = f"checkpoint_{index+1}.json"
                with open(checkpoint_file, 'w', encoding='utf-8') as f:
                    json.dump(todos_resultados, f, ensure_ascii=False, indent=2)
                print(f"  ✅ Checkpoint salvo em {checkpoint_file}")
            
        except Exception as e:
            total_erro += 1
            print(f"  ❌ Erro crítico: {str(e)}")
            todos_resultados.append({
                'url': link,
                'nome_original_planilha': nome,
                'status': 'erro',
                'motivo': str(e)
            })
        
        # Pequeno delay entre requisições
        time.sleep(1)
    
    # Fechar driver
    driver.quit()
    
    # Estatísticas finais
    print("\n" + "="*60)
    print("📊 RESUMO DA EXTRAÇÃO")
    print("="*60)
    print(f"Total processados: {len(df)}")
    print(f"✅ Sucesso: {total_sucesso}")
    print(f"❌ Erros: {total_erro}")
    print(f"📈 Taxa de sucesso: {total_sucesso/len(df)*100:.1f}%")
    print("="*60)
    
    # Salvar resultados finais
    if todos_resultados:
        arquivo_salvo = salvar_resultados(todos_resultados)
        print(f"\n✨ Arquivo salvo com sucesso!")
        
        # Mostrar algumas estatísticas adicionais
        df_resultados = pd.DataFrame(todos_resultados)
        if 'status' in df_resultados.columns:
            df_sucesso = df_resultados[df_resultados['status'] == 'sucesso']
            
            if not df_sucesso.empty:
                print("\n📈 Estatísticas dos dados extraídos:")
                print(f"  Empresas com email: {df_sucesso['emails'].apply(lambda x: len(x) > 0).sum()}")
                print(f"  Empresas com telefone: {df_sucesso['telefones'].apply(lambda x: len(x) > 0).sum()}")
                print(f"  Empresas com website: {df_sucesso['websites'].apply(lambda x: len(x) > 0).sum()}")
                print(f"  Empresas com redes sociais: {df_sucesso['redes_sociais'].apply(lambda x: any(x.values())).sum()}")
                print(f"  Média de produtos por empresa: {df_sucesso['produtos_detectados'].apply(len).mean():.1f}")
                print(f"  Média de membros da equipe: {df_sucesso['equipe_extraida'].apply(len).mean():.1f}")
    else:
        print("\n⚠️ Nenhum dado foi extraído!")