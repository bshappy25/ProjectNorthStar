"""
ONYX Elite Module - Maximum Security Clearance
Ultra-exclusive access for elite operatives only
"""

import streamlit as st
import time
import random
from datetime import datetime

def render(admin_unlocked):
    """Render the ONYX Elite interface"""
    
    # Maximum security check
    if not admin_unlocked:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; 
                        background: rgba(20, 20, 20, 0.95);
                        backdrop-filter: blur(30px); border-radius: 30px; 
                        border: 3px solid rgba(255, 0, 0, 0.5);
                        box-shadow: 0 0 60px rgba(255, 0, 0, 0.3),
                                    inset 0 0 80px rgba(0, 0, 0, 0.8);">
                <div style="font-size: 6rem; margin-bottom: 1rem; 
                            filter: drop-shadow(0 0 30px rgba(255, 0, 0, 0.8));">⚫</div>
                <h1 style="color: rgba(255, 0, 0, 0.9); font-size: 3rem; margin-bottom: 1rem;
                            text-shadow: 0 0 30px rgba(255, 0, 0, 0.8); letter-spacing: 6px;">
                    ELITE ACCESS DENIED
                </h1>
                <p style="color: rgba(255, 0, 0, 0.8); font-size: 1.5rem; margin-bottom: 2rem;">
                    ⛔ MAXIMUM SECURITY CLEARANCE REQUIRED ⛔
                </p>
                <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.2rem; line-height: 1.8; font-family: monospace;">
                    [CLASSIFIED]<br/>
                    This area is restricted to ONYX Elite operatives.<br/>
                    Palm ID authentication mandatory.<br/><br/>
                    <span style="color: rgba(255, 0, 0, 0.9); font-weight: bold;">
                    >>> RETURN TO HUB AND UNLOCK ACCESS <<<
                    </span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # ELITE STYLING
    st.markdown("""
        <style>
            .elite-header {
                text-align: center;
                padding: 3rem 2rem;
                background: rgba(20, 20, 20, 0.95);
                backdrop-filter: blur(30px);
                border-radius: 30px;
                border: 3px solid rgba(100, 255, 255, 0.5);
                box-shadow: 0 0 80px rgba(100, 255, 255, 0.3),
                            inset 0 0 100px rgba(0, 0, 0, 0.8);
                margin-bottom: 2rem;
                position: relative;
            }
            
            .elite-icon {
                font-size: 5rem;
                filter: drop-shadow(0 0 50px rgba(100, 255, 255, 0.8));
                animation: elite-pulse 2s ease-in-out infinite;
            }
            
            @keyframes elite-pulse {
                0%, 100% { 
                    filter: drop-shadow(0 0 50px rgba(100, 255, 255, 0.8));
                    transform: scale(1) rotate(0deg);
                }
                50% { 
                    filter: drop-shadow(0 0 80px rgba(100, 255, 255, 1));
                    transform: scale(1.1) rotate(180deg);
                }
            }
            
            .elite-title {
                font-size: 3.5rem;
                font-weight: 900;
                background: linear-gradient(135deg, #64ffff 0%, #ffffff 50%, #64ffff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: 10px;
                margin: 1rem 0;
                text-shadow: 0 0 50px rgba(100, 255, 255, 0.5);
            }
            
            .clearance-badge {
                display: inline-block;
                padding: 0.8rem 2rem;
                background: linear-gradient(135deg, rgba(100, 255, 255, 0.3) 0%, rgba(100, 255, 255, 0.2) 100%);
                color: rgba(100, 255, 255, 0.9);
                border-radius: 50px;
                font-weight: 900;
                font-size: 1.2rem;
                letter-spacing: 4px;
                box-shadow: 0 0 40px rgba(100, 255, 255, 0.4);
                border: 2px solid rgba(100, 255, 255, 0.6);
                text-transform: uppercase;
            }
            
            .elite-card {
                background: rgba(20, 20, 20, 0.95);
                backdrop-filter: blur(25px);
                border: 2px solid rgba(100, 255, 255, 0.3);
                border-radius: 25px;
                padding: 2.5rem;
                margin: 2rem 0;
                box-shadow: 0 0 50px rgba(100, 255, 255, 0.2),
                            inset 0 0 60px rgba(0, 0, 0, 0.8);
            }
            
            .elite-card:hover {
                border-color: rgba(100, 255, 255, 0.6);
                box-shadow: 0 0 80px rgba(100, 255, 255, 0.4);
            }
            
            .stat-elite {
                background: rgba(100, 255, 255, 0.05);
                border: 2px solid rgba(100, 255, 255, 0.3);
                border-radius: 20px;
                padding: 2rem 1.5rem;
                text-align: center;
            }
            
            .stat-elite:hover {
                background: rgba(100, 255, 255, 0.1);
                border-color: rgba(100, 255, 255, 0.6);
                box-shadow: 0 0 30px rgba(100, 255, 255, 0.3);
            }
            
            .elite-number {
                font-size: 3rem;
                font-weight: 900;
                color: rgba(100, 255, 255, 0.9);
                text-shadow: 0 0 20px rgba(100, 255, 255, 0.5);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize elite session state
    if 'elite_sessions' not in st.session_state:
        st.session_state.elite_sessions = 0
    if 'elite_operations' not in st.session_state:
        st.session_state.elite_operations = 0
    if 'elite_clearance_date' not in st.session_state:
        st.session_state.elite_clearance_date = datetime.now().strftime("%Y-%m-%d")
    
    st.session_state.elite_sessions += 1
    
    # ELITE HEADER
    st.markdown("""
        <div class="elite-header">
            <div class="elite-icon">💠</div>
            <h1 class="elite-title">ONYX ELITE</h1>
            <div class="clearance-badge">⚫ MAXIMUM CLEARANCE ⚫</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Clearance confirmation
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="elite-card">
            <h2 style="color: rgba(100, 255, 255, 0.9); text-align: center; margin-bottom: 1rem; letter-spacing: 3px;">
                ⚡ CLEARANCE CONFIRMED ⚡
            </h2>
            <p style="text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 1.1rem; 
                      line-height: 1.8; font-family: monospace;">
                OPERATIVE STATUS: <strong style="color: rgba(100, 255, 255, 0.9);">ACTIVE</strong><br/>
                SYSTEM TIME: {current_time}<br/>
                CLEARANCE DATE: {st.session_state.elite_clearance_date}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Elite Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-elite">
                <div class="elite-number">{st.session_state.elite_sessions}</div>
                <div style="color: rgba(100, 255, 255, 0.7); margin-top: 0.5rem; font-size: 0.9rem; letter-spacing: 2px;">
                    SESSIONS
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-elite">
                <div class="elite-number">{st.session_state.elite_operations}</div>
                <div style="color: rgba(100, 255, 255, 0.7); margin-top: 0.5rem; font-size: 0.9rem; letter-spacing: 2px;">
                    OPERATIONS
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        threat_level = max(0, 100 - st.session_state.elite_operations * 5)
        st.markdown(f"""
            <div class="stat-elite">
                <div class="elite-number">{threat_level}%</div>
                <div style="color: rgba(100, 255, 255, 0.7); margin-top: 0.5rem; font-size: 0.9rem; letter-spacing: 2px;">
                    STEALTH
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-elite">
                <div class="elite-number">MAX</div>
                <div style="color: rgba(100, 255, 255, 0.7); margin-top: 0.5rem; font-size: 0.9rem; letter-spacing: 2px;">
                    CLEARANCE
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Elite Operations
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs([
        "💠 COMMAND CENTER",
        "🎯 BLACK OPS",
        "🔒 CLASSIFIED"
    ])
    
    with tab1:
        st.markdown("""
            <div class="elite-card">
                <h3 style="color: rgba(100, 255, 255, 0.9); margin-bottom: 1.5rem; letter-spacing: 2px;">
                    💠 ELITE COMMAND CENTER
                </h3>
                <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                    Advanced operational dashboard for maximum clearance personnel.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        operation_type = st.selectbox(
            "SELECT OPERATION TYPE:",
            ["🎯 Intelligence Gathering", "🔐 Secure Communications", "💎 Asset Management", "⚡ Rapid Deployment"],
            key="op_type"
        )
        
        if st.button("🚀 INITIATE OPERATION", key="init_op", type="primary"):
            st.session_state.elite_operations += 1
            with st.spinner("⚡ EXECUTING..."):
                time.sleep(1.5)
            st.success(f"✅ OPERATION SUCCESSFUL • STATUS: COMPLETE")
            st.balloons()
    
    with tab2:
        st.markdown("""
            <div class="elite-card">
                <h3 style="color: rgba(100, 255, 255, 0.9); margin-bottom: 1.5rem; letter-spacing: 2px;">
                    🎯 BLACK OPS MISSIONS
                </h3>
                <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                    Covert operations requiring maximum security clearance.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        missions = [
            {"name": "OPERATION NIGHTFALL", "difficulty": "EXTREME", "status": "READY"},
            {"name": "OPERATION SHADOWSTRIKE", "difficulty": "CRITICAL", "status": "READY"},
            {"name": "OPERATION DARKNET", "difficulty": "CLASSIFIED", "status": "STANDBY"},
            {"name": "OPERATION PHANTOM", "difficulty": "MAXIMUM", "status": "READY"}
        ]
        
        for mission in missions:
            difficulty_color = {
                "EXTREME": "rgba(255, 100, 100, 0.9)",
                "CRITICAL": "rgba(255, 200, 100, 0.9)",
                "CLASSIFIED": "rgba(100, 255, 255, 0.9)",
                "MAXIMUM": "rgba(200, 100, 255, 0.9)"
            }.get(mission["difficulty"], "rgba(100, 255, 255, 0.9)")
            
            st.markdown(f"""
                <div style="background: rgba(20, 20, 20, 0.8); padding: 1.5rem; border-radius: 15px;
                            border: 2px solid rgba(100, 255, 255, 0.2); margin: 1rem 0;">
                    <div style="display: grid; grid-template-columns: auto 1fr auto; gap: 1.5rem; align-items: center;">
                        <div style="font-size: 2rem;">🎯</div>
                        <div>
                            <p style="color: rgba(100, 255, 255, 0.9); margin: 0; font-weight: 700; font-size: 1.1rem;">
                                {mission["name"]}
                            </p>
                            <p style="color: {difficulty_color}; margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                                DIFFICULTY: {mission["difficulty"]}
                            </p>
                        </div>
                        <div>
                            <p style="color: rgba(100, 255, 255, 0.7); margin: 0; font-size: 0.9rem;">
                                {mission["status"]}
                            </p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
            <div class="elite-card">
                <h3 style="color: rgba(100, 255, 255, 0.9); margin-bottom: 1.5rem; letter-spacing: 2px;">
                    🔒 CLASSIFIED INTEL
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        intel_messages = [
            "SIGNAL INTERCEPT: INCOMING TRANSMISSION DETECTED",
            "NETWORK ANALYSIS: ALL SYSTEMS SECURE",
            "THREAT ASSESSMENT: MINIMAL RISK LEVEL",
            "ELITE STATUS: FULLY OPERATIONAL",
            "CLEARANCE VERIFIED: MAXIMUM AUTHORITY CONFIRMED"
        ]
        
        selected_intel = random.choice(intel_messages)
        
        st.markdown(f"""
            <div style="background: rgba(20, 20, 20, 0.9); padding: 2rem; border-radius: 20px;
                        border: 2px solid rgba(100, 255, 255, 0.3); text-align: center;
                        box-shadow: 0 0 40px rgba(100, 255, 255, 0.2);">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔒</div>
                <p style="color: rgba(100, 255, 255, 0.9); font-size: 1.3rem; font-family: monospace; line-height: 1.8;">
                    {selected_intel}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 REFRESH INTEL", key="refresh_intel"):
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; background: rgba(20, 20, 20, 0.8);
                    backdrop-filter: blur(10px); border-radius: 20px; 
                    border: 2px solid rgba(100, 255, 255, 0.2);">
            <p style="color: rgba(100, 255, 255, 0.7); font-size: 0.95rem; margin: 0; font-family: monospace;">
                SESSION: {st.session_state.elite_sessions} • OPERATIONS: {st.session_state.elite_operations} • 
                CLEARANCE: MAXIMUM ⚫
            </p>
        </div>
    """, unsafe_allow_html=True)
