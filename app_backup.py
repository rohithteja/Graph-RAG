"""
Interactive Graph RAG vs Traditional RAG Demo
"""
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from plotly.subplots import make_subplots
from knowledge_graph import SuperheroGraph
from simple_rag import SimpleTraditionalRAG, SimpleGraphRAG, create_superhero_documents

# Page configuration
st.set_page_config(
    page_title="🦸‍♂️ Graph RAG vs Traditional RAG",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'traditional_rag' not in st.session_state:
    st.session_state.traditional_rag = None
if 'graph_rag' not in st.session_state:
    st.session_state.graph_rag = None
if 'neo4j_graph' not in st.session_state:
    st.session_state.neo4j_graph = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'show_rag_structure' not in st.session_state:
    st.session_state.show_rag_structure = True
if 'show_graph_viz' not in st.session_state:
    st.session_state.show_graph_viz = True

def create_graph_visualization(graph_data):
    """Create an interactive graph visualization using Plotly"""
    if not graph_data or not graph_data['nodes']:
        return None
    
    # Create NetworkX graph
    G = nx.Graph()
    
    # Add nodes
    node_colors = []
    node_sizes = []
    node_text = []
    
    for node in graph_data['nodes']:
        node_id = node['id']
        props = node['properties']
        G.add_node(node_id, **props)
        
        # Color by type
        if 'Hero' in node['labels']:
            node_colors.append('red')
            node_sizes.append(30)
            node_text.append(f"🦸‍♂️ {props.get('name', node_id)}")
        elif 'Team' in node['labels']:
            node_colors.append('blue')
            node_sizes.append(25)
            node_text.append(f"👥 {props.get('name', node_id)}")
        else:
            node_colors.append('gray')
            node_sizes.append(20)
            node_text.append(props.get('name', node_id))
    
    # Add edges
    edge_trace = []
    for rel in graph_data['relationships']:
        source_id = rel['source']
        target_id = rel['target']
        G.add_edge(source_id, target_id, type=rel['type'])
    
    # Use spring layout for positioning
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create the plot
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='lightgray'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Add nodes
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        hovertext=[f"{text}<br>Connections: {len(list(G.neighbors(node)))}" 
                  for node, text in zip(G.nodes(), node_text)],
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='white'),
            opacity=0.8
        )
    ))
    
    # Add relationship labels
    for rel in graph_data['relationships']:
        source_pos = pos[rel['source']]
        target_pos = pos[rel['target']]
        mid_x = (source_pos[0] + target_pos[0]) / 2
        mid_y = (source_pos[1] + target_pos[1]) / 2
        
        fig.add_annotation(
            x=mid_x, y=mid_y,
            text=rel['type'],
            showarrow=False,
            font=dict(size=8, color="darkgreen"),
            bgcolor="white",
            bordercolor="green",
            borderwidth=1
        )
    
    fig.update_layout(
        title="🕸️ Graph RAG: Knowledge Graph Structure",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[
            dict(
                text="Interactive: Hover over nodes to see connections",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=10)
            )
        ],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=500
    )
    
    return fig

def initialize_systems():
    """Initialize both RAG systems"""
    try:
        with st.spinner("🔄 Initializing systems..."):
            # Initialize Traditional RAG
            st.session_state.traditional_rag = SimpleTraditionalRAG()
            docs = create_superhero_documents()
            st.session_state.traditional_rag.add_documents(docs)
            
            # Initialize Neo4j Graph
            st.session_state.neo4j_graph = SuperheroGraph()
            st.session_state.neo4j_graph.clear_graph()
            st.session_state.neo4j_graph.create_superhero_graph()
            
            # Initialize Graph RAG
            st.session_state.graph_rag = SimpleGraphRAG(st.session_state.neo4j_graph)
            
            st.session_state.initialized = True
            st.success("✅ Both systems initialized successfully!")
            
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        st.error("Make sure Neo4j is running on localhost:7687 with auth neo4j/password")

def main():
    """Clean, organized Streamlit app for RAG comparison"""
    
    # Header
    st.title("🦸‍♂️ Graph RAG vs Traditional RAG Demo")
    st.markdown("### 🎯 Compare Two Approaches to Information Retrieval")
    
    # Sidebar for navigation and setup
    with st.sidebar:
        st.header("🛠️ Setup")
        
        if not st.session_state.initialized:
            st.warning("⚠️ Systems not initialized")
            if st.button("🚀 Initialize Systems"):
                initialize_systems()
        else:
            st.success("✅ Systems ready!")
            
            if st.button("🔄 Reinitialize"):
                st.session_state.initialized = False
                st.rerun()
        
        st.markdown("---")
        st.header("� Views")
        
        st.session_state.show_rag_structure = st.checkbox("📚 Show RAG Structure", value=True)
        st.session_state.show_graph_viz = st.checkbox("🕸️ Show Graph Visualization", value=True)
        
        st.markdown("---")
        st.header("ℹ️ Info")
        st.markdown("""
        **🔵 Traditional RAG:**
        - Document-based search
        - Keyword matching
        - Good for facts
        
        **🔴 Graph RAG:**
        - Relationship-based
        - Network traversal  
        - Good for connections
        """)
    
    # Show structure visualization first
    if st.session_state.show_rag_structure:
        st.header("📊 RAG Structures Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Traditional RAG Structure")
            st.markdown("**Simple Document Storage - Plain Text:**")
            
            # Show actual documents as plain text
            docs = create_superhero_documents()
            
            # Create a scrollable container with all documents
            document_text = ""
            for i, doc in enumerate(docs, 1):
                document_text += f"📄 **Document {i}: {doc['title']}**\n"
                document_text += f"Character: {doc.get('character', 'N/A')}\n"
                document_text += f"Content: {doc['content']}\n"
                document_text += "\n" + "="*50 + "\n\n"
            
            st.text_area(
                "Document Database Contents:",
                value=document_text,
                height=400,
                disabled=True,
                help="This is how Traditional RAG stores information - as plain text documents"
            )
            
            with st.expander("ℹ️ How Traditional RAG Works"):
                st.markdown("""
                **Process:**
                1. 📄 Store documents as plain text in database
                2. 🔍 User asks a question
                3. 🎯 Find most relevant documents using keyword matching
                4. 📝 Return top matching documents
                
                **Good for:** Direct facts, definitions, descriptions
                **Simple:** Just text search - no relationships!
                """)
        
        with col2:
            if st.session_state.initialized and st.session_state.show_graph_viz:
                st.subheader("🕸️ Graph RAG Structure")
                try:
                    graph_data = st.session_state.neo4j_graph.visualize_graph()
                    graph_fig = create_graph_visualization(graph_data)
                    if graph_fig:
                        st.plotly_chart(graph_fig, use_container_width=True)
                    
                    with st.expander("ℹ️ How Graph RAG Works"):
                        st.markdown("""
                        **Process:**
                        1. 🕸️ Store entities and relationships in graph
                        2. 🔍 User asks a question
                        3. 🎯 Find relevant entities and traverse connections
                        4. 📊 Return connected information paths
                        
                        **Good for:** Relationships, connections, complex reasoning
                        """)
                        
                except Exception as e:
                    st.error(f"Graph visualization error: {str(e)}")
            else:
                st.info("🔄 Initialize systems to see graph structure")
    
    # Main content - only show if initialized
    if not st.session_state.initialized:
        st.markdown("---")
        st.warning("⚠️ Please initialize the systems using the sidebar to start comparing RAG approaches")
        
        # Show what will be available
        st.markdown("### 🎮 What You'll Be Able To Do:")
        st.markdown("""
        - 🔍 **Try Different Queries** - Ask questions about superheroes
        - 📊 **Compare Results** - See how each RAG approach responds  
        - 🦸‍♂️ **Explore Data** - View the superhero knowledge base
        - 📈 **Understand Differences** - Learn when to use each approach
        """)
        return
    
    # Query interface
    st.markdown("---")
    st.header("🔍 Interactive Query Comparison")
    
    # Sample queries with explanations
    sample_queries = {
        "What are Superman's powers?": "📄 Best for Traditional RAG - Direct factual question",
        "Who are Batman's teammates?": "🕸️ Best for Graph RAG - Relationship question",
        "Tell me about Wonder Woman's abilities": "📄 Best for Traditional RAG - Description request",
        "How is Superman connected to other heroes?": "🕸️ Best for Graph RAG - Connection analysis",
        "What is the Justice League?": "📄 Best for Traditional RAG - Definition question",
        "Show me all Justice League relationships": "🕸️ Best for Graph RAG - Network exploration"
    }
    
    # Query input with better UX
    st.markdown("### 💬 Ask a Question")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_input("Enter your query:", placeholder="Ask about superheroes...", key="query_input")
    
    with col2:
        selected_sample = st.selectbox("📝 Sample Questions:", ["Choose a sample..."] + list(sample_queries.keys()))
        
    if selected_sample != "Choose a sample...":
        query = selected_sample
        st.info(f"💡 {sample_queries[selected_sample]}")
    
    if query:
        st.markdown("---")
        st.markdown("### 🔄 Comparing RAG Approaches")
        
        # Create tabs for better organization
        tab1, tab2, tab3 = st.tabs(["📊 Side-by-Side", "📄 Traditional Details", "🕸️ Graph Details"])
        
        with tab1:
            # Side by side comparison
            col1, col2 = st.columns(2)
            
            # Traditional RAG Results
            with col1:
                st.markdown("#### 📄 Traditional RAG Results")
                with st.container():
                    try:
                        traditional_results = st.session_state.traditional_rag.search(query, top_k=3)
                        
                        if traditional_results:
                            # Show summary first
                            st.success(f"✅ Found {len(traditional_results)} matching documents")
                            
                            # Show top result prominently
                            best_result = traditional_results[0]
                            st.markdown(f"**🥇 Best Match:** {best_result['title']}")
                            st.markdown(f"**🎯 Relevance:** {best_result['similarity']:.1f}/1.0")
                            st.text_area("Content Preview:", 
                                       value=best_result['content'][:200] + "...", 
                                       height=100, 
                                       disabled=True)
                            
                            # Show all results in expander
                            with st.expander(f"📋 View All {len(traditional_results)} Results"):
                                for i, result in enumerate(traditional_results):
                                    st.markdown(f"**{i+1}. {result['title']}** (Score: {result['similarity']:.3f})")
                                    st.text(result['content'][:150] + "...")
                                    st.markdown("---")
                        else:
                            st.warning("⚠️ No matching documents found")
                            
                    except Exception as e:
                        st.error(f"❌ Traditional RAG error: {str(e)}")
            
            # Graph RAG Results
            with col2:
                st.markdown("#### 🕸️ Graph RAG Results")
                with st.container():
                    try:
                        graph_results = st.session_state.graph_rag.search(query)
                        
                        if graph_results:
                            st.success(f"✅ Found {len(graph_results)} connected entities")
                            
                            # Show connection summary
                            entity_types = {}
                            for result in graph_results:
                                if 'teammate' in result:
                                    entity_types['teammates'] = entity_types.get('teammates', 0) + 1
                                elif 'hero' in result:
                                    entity_types['heroes'] = entity_types.get('heroes', 0) + 1
                                elif 'name' in result:
                                    entity_types['entities'] = entity_types.get('entities', 0) + 1
                            
                            st.markdown("**🔗 Connection Summary:**")
                            for entity_type, count in entity_types.items():
                                st.markdown(f"- {entity_type.title()}: {count}")
                            
                            # Show results
                            with st.expander(f"🕸️ View All {len(graph_results)} Connections"):
                                for i, result in enumerate(graph_results):
                                    st.markdown(f"**Connection {i+1}:**")
                                    st.json(result)
                                    
                        else:
                            st.warning("⚠️ No graph connections found")
                            
                    except Exception as e:
                        st.error(f"❌ Graph RAG error: {str(e)}")
        
        with tab2:
            st.markdown("#### 📄 Traditional RAG Deep Dive")
            try:
                traditional_results = st.session_state.traditional_rag.search(query, top_k=5)
                if traditional_results:
                    # Show detailed analysis
                    df = pd.DataFrame([{
                        'Document': r['title'],
                        'Character': r.get('character', 'N/A'),
                        'Relevance Score': r['similarity'],
                        'Content Length': len(r['content'])
                    } for r in traditional_results])
                    
                    st.dataframe(df, use_container_width=True)
                    
                    # Show full content of selected document
                    selected_doc = st.selectbox("Select document to view full content:", 
                                               [r['title'] for r in traditional_results])
                    
                    if selected_doc:
                        selected_result = next(r for r in traditional_results if r['title'] == selected_doc)
                        st.text_area("Full Document Content:", 
                                   value=selected_result['content'], 
                                   height=200, 
                                   disabled=True)
                else:
                    st.info("No traditional RAG results to analyze")
            except Exception as e:
                st.error(f"Error in traditional RAG analysis: {str(e)}")
        
        with tab3:
            st.markdown("#### 🕸️ Graph RAG Deep Dive")
            try:
                graph_results = st.session_state.graph_rag.search(query)
                if graph_results:
                    st.markdown("**🔍 Graph Traversal Analysis:**")
                    
                    # Analyze the type of connections found
                    connection_analysis = {
                        'Direct Matches': 0,
                        'Relationship Connections': 0,
                        'Team Connections': 0
                    }
                    
                    for result in graph_results:
                        if 'teammate' in result or 'relationship' in result:
                            connection_analysis['Relationship Connections'] += 1
                        elif 'hero' in result and 'powers' in result:
                            connection_analysis['Direct Matches'] += 1
                        else:
                            connection_analysis['Team Connections'] += 1
                    
                    # Show analysis as metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Direct Matches", connection_analysis['Direct Matches'])
                    with col2:
                        st.metric("Relationships", connection_analysis['Relationship Connections'])
                    with col3:
                        st.metric("Team Links", connection_analysis['Team Connections'])
                    
                    # Detailed results
                    st.markdown("**📊 Detailed Graph Results:**")
                    for i, result in enumerate(graph_results, 1):
                        with st.expander(f"Graph Path {i}"):
                            st.json(result)
                else:
                    st.info("No graph RAG results to analyze")
            except Exception as e:
                st.error(f"Error in graph RAG analysis: {str(e)}")
    
    # Data Explorer Section
    st.markdown("---")
    st.header("🗃️ Data Explorer")
    
    explorer_tab1, explorer_tab2 = st.tabs(["📄 Document Database", "🕸️ Knowledge Graph"])
    
    with explorer_tab1:
        st.subheader("📚 Traditional RAG Document Store")
        
        if st.session_state.initialized:
            docs = create_superhero_documents()
            
            # Document overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 Total Documents", len(docs))
            with col2:
                total_chars = sum(len(doc['content']) for doc in docs)
                st.metric("📝 Total Characters", f"{total_chars:,}")
            with col3:
                unique_heroes = len(set(doc.get('character', 'Unknown') for doc in docs))
                st.metric("🦸‍♂️ Heroes Covered", unique_heroes)
            
            # Document browser
            st.markdown("**📖 Browse Documents:**")
            selected_doc_title = st.selectbox("Select document:", [doc['title'] for doc in docs])
            
            if selected_doc_title:
                selected_doc = next(doc for doc in docs if doc['title'] == selected_doc_title)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.text_area("Content:", value=selected_doc['content'], height=200, disabled=True)
                with col2:
                    st.markdown("**📋 Metadata:**")
                    st.write(f"**ID:** {selected_doc['id']}")
                    st.write(f"**Character:** {selected_doc.get('character', 'N/A')}")
                    st.write(f"**Length:** {len(selected_doc['content'])} chars")
        else:
            st.info("� Initialize systems to explore documents")
    
    with explorer_tab2:
        st.subheader("🕸️ Knowledge Graph Database")
        
        if st.session_state.initialized:
            try:
                graph_data = st.session_state.neo4j_graph.visualize_graph()
                
                # Graph statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🔵 Nodes", len(graph_data['nodes']))
                with col2:
                    st.metric("🔗 Relationships", len(graph_data['relationships']))
                with col3:
                    hero_count = sum(1 for n in graph_data['nodes'] if 'Hero' in n['labels'])
                    st.metric("🦸‍♂️ Heroes", hero_count)
                with col4:
                    team_count = sum(1 for n in graph_data['nodes'] if 'Team' in n['labels'])
                    st.metric("👥 Teams", team_count)
                
                # Interactive graph
                if st.session_state.show_graph_viz:
                    graph_fig = create_graph_visualization(graph_data)
                    if graph_fig:
                        st.plotly_chart(graph_fig, use_container_width=True)
                
                # Data tables
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🦸‍♂️ Heroes in Graph:**")
                    heroes_data = []
                    for node in graph_data['nodes']:
                        if 'Hero' in node['labels']:
                            props = node['properties']
                            heroes_data.append({
                                'Hero': props.get('name', ''),
                                'Real Name': props.get('real_name', ''),
                                'Origin': props.get('origin', ''),
                                'Team': props.get('team', '')
                            })
                    
                    if heroes_data:
                        st.dataframe(pd.DataFrame(heroes_data), use_container_width=True)
                
                with col2:
                    st.markdown("**🔗 Relationships:**")
                    rels_data = []
                    for rel in graph_data['relationships']:
                        source_node = next((n for n in graph_data['nodes'] if n['id'] == rel['source']), None)
                        target_node = next((n for n in graph_data['nodes'] if n['id'] == rel['target']), None)
                        
                        if source_node and target_node:
                            rels_data.append({
                                'From': source_node['properties'].get('name', 'Unknown'),
                                'Type': rel['type'],
                                'To': target_node['properties'].get('name', 'Unknown')
                            })
                    
                    if rels_data:
                        st.dataframe(pd.DataFrame(rels_data), use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ Graph visualization error: {str(e)}")
        else:
            st.info("🔄 Initialize systems to explore the knowledge graph")
    
    # Documentation
    st.markdown("---")
    st.header("📚 How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Traditional RAG")
        st.markdown("""
        **Process:**
        1. Documents are embedded using sentence transformers
        2. Query is embedded using the same model
        3. Cosine similarity finds most relevant documents
        4. Top-k documents are returned
        
        **Good for:**
        - Factual questions
        - Direct information retrieval
        - When relationships don't matter
        """)
    
    with col2:
        st.subheader("🕸️ Graph RAG")
        st.markdown("""
        **Process:**
        1. Entities and relationships are stored in Neo4j
        2. Query is analyzed for entity mentions
        3. Graph traversal finds connected information
        4. Related nodes and paths are returned
        
        **Good for:**
        - Relationship questions
        - Connected information
        - Complex reasoning over connections
        """)

if __name__ == "__main__":
    main()
