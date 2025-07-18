"""Data Analyst Agent

Specialized agent for data analysis, visualization, and insights generation.
Uses pandas, DuckDB, and other data tools to analyze datasets and answer questions.
"""

from typing import Any, Dict, List, Optional, Union

import duckdb
import pandas as pd
from pydantic import BaseModel, Field

from src.agents.base import AgentRole, BaseAgent, AgentResponse


class DataAnalysisRequest(BaseModel):
    """Request for data analysis"""
    
    question: str = Field(description="The question to answer about the data")
    sql_query: Optional[str] = Field(None, description="Optional SQL query to run")
    visualization_type: Optional[str] = Field(None, description="Type of viz to create")
    groupby: Optional[List[str]] = Field(None, description="Columns to group by")
    aggregations: Optional[Dict[str, str]] = Field(None, description="Aggregations to perform")


class DataInsight(BaseModel):
    """A single data insight"""
    
    insight: str = Field(description="The insight discovered")
    importance: float = Field(ge=0.0, le=1.0, description="Importance score")
    evidence: str = Field(description="Supporting evidence")
    visualization: Optional[str] = Field(None, description="Related visualization")


class DataAnalysisResponse(BaseModel):
    """Response from data analysis"""
    
    summary: str = Field(description="Executive summary of findings")
    insights: List[DataInsight] = Field(description="Key insights discovered")
    statistics: Dict[str, Any] = Field(description="Relevant statistics")
    visualizations: List[str] = Field(default_factory=list, description="Generated viz")
    recommendations: List[str] = Field(description="Recommended actions")
    confidence: float = Field(ge=0.0, le=1.0)
    sql_used: Optional[str] = Field(None, description="SQL query used")


class DataQualityReport(BaseModel):
    """Report on data quality"""
    
    total_rows: int
    total_columns: int
    missing_values: Dict[str, int]
    duplicate_rows: int
    data_types: Dict[str, str]
    quality_score: float = Field(ge=0.0, le=1.0)
    issues: List[str]
    recommendations: List[str]


class DataAnalystAgent(BaseAgent):
    """Agent specialized in data analysis and insights"""
    
    role: AgentRole = AgentRole.DATA_ANALYST
    name: str = "Data Analyst"
    description: str = (
        "I analyze datasets to uncover insights, create visualizations, "
        "and provide data-driven recommendations. I excel at SQL, statistics, "
        "and explaining complex findings in simple terms."
    )
    tools: List[str] = [
        "pandas",
        "duckdb",
        "numpy",
        "scipy",
        "plotly",
        "data_profiling",
        "statistical_tests"
    ]
    
    def analyze_dataframe(
        self,
        df: pd.DataFrame,
        request: DataAnalysisRequest
    ) -> DataAnalysisResponse:
        """Analyze a pandas DataFrame"""
        # First, understand the data structure
        context = self._build_dataframe_context(df)
        
        # Create analysis prompt
        prompt = f"""
Analyze this dataset to answer: {request.question}

Dataset shape: {df.shape}
Columns: {', '.join(df.columns)}
Data types: {df.dtypes.to_dict()}
First few rows: {df.head().to_dict()}
Basic statistics: {df.describe().to_dict() if not df.empty else 'Empty dataset'}

{f"Run this SQL: {request.sql_query}" if request.sql_query else ""}
{f"Create {request.visualization_type} visualization" if request.visualization_type else ""}
{f"Group by: {request.groupby}" if request.groupby else ""}
{f"Aggregate: {request.aggregations}" if request.aggregations else ""}

Provide:
1. Executive summary answering the question
2. Key insights with importance scores
3. Relevant statistics
4. Visualization descriptions
5. Actionable recommendations
"""
        
        # Get structured response
        response = self.think(
            prompt=prompt,
            response_model=DataAnalysisResponse,
            context=context
        )
        
        # If SQL was requested, execute it
        if request.sql_query:
            sql_result = self.execute_sql(df, request.sql_query)
            if sql_result is not None:
                # Re-analyze with SQL results
                sql_context = self._build_dataframe_context(sql_result)
                response = self.think(
                    prompt=f"Refine analysis with SQL results: {sql_context}",
                    response_model=DataAnalysisResponse,
                    context={**context, "sql_result": sql_context}
                )
        
        return response
    
    def profile_data(self, df: pd.DataFrame) -> DataQualityReport:
        """Generate a data quality report"""
        # Calculate quality metrics
        total_rows = len(df)
        total_columns = len(df.columns)
        missing_values = df.isnull().sum().to_dict()
        duplicate_rows = df.duplicated().sum()
        data_types = df.dtypes.astype(str).to_dict()
        
        # Calculate quality score
        total_cells = total_rows * total_columns
        missing_cells = sum(missing_values.values())
        quality_score = 1.0 - (missing_cells / total_cells) if total_cells > 0 else 0.0
        
        # Identify issues
        issues = []
        if missing_cells > 0:
            issues.append(f"{missing_cells} missing values across {sum(v > 0 for v in missing_values.values())} columns")
        if duplicate_rows > 0:
            issues.append(f"{duplicate_rows} duplicate rows found")
        
        # Get recommendations from AI
        prompt = f"""
Based on this data quality report, provide recommendations:
- Total rows: {total_rows}
- Missing values: {missing_values}
- Duplicate rows: {duplicate_rows}
- Data types: {data_types}
- Issues: {issues}

What should be done to improve data quality?
"""
        
        recommendations_response = self.think(
            prompt=prompt,
            response_model=AgentResponse
        )
        
        return DataQualityReport(
            total_rows=total_rows,
            total_columns=total_columns,
            missing_values=missing_values,
            duplicate_rows=duplicate_rows,
            data_types=data_types,
            quality_score=quality_score,
            issues=issues,
            recommendations=recommendations_response.next_steps
        )
    
    def execute_sql(
        self,
        df: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        query: str
    ) -> Optional[pd.DataFrame]:
        """Execute SQL query using DuckDB"""
        try:
            # Create in-memory DuckDB connection
            conn = duckdb.connect(":memory:")
            
            # Register DataFrame(s)
            if isinstance(df, pd.DataFrame):
                conn.register("data", df)
            else:
                # Multiple tables
                for table_name, table_df in df.items():
                    conn.register(table_name, table_df)
            
            # Execute query
            result = conn.execute(query).fetchdf()
            conn.close()
            
            return result
            
        except Exception as e:
            self.memory.add_interaction(
                "system",
                f"SQL error: {str(e)}"
            )
            return None
    
    def find_correlations(
        self,
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        threshold: float = 0.5
    ) -> Dict[str, float]:
        """Find correlations in the data"""
        # Get numeric columns only
        numeric_df = df.select_dtypes(include=["int64", "float64"])
        
        if numeric_df.empty:
            return {}
        
        # Calculate correlations
        if target_column and target_column in numeric_df.columns:
            correlations = numeric_df.corr()[target_column].abs()
            correlations = correlations[correlations > threshold]
            correlations = correlations.drop(target_column).sort_values(ascending=False)
        else:
            # Find all strong correlations
            corr_matrix = numeric_df.corr().abs()
            upper_triangle = corr_matrix.where(
                pd.np.triu(pd.np.ones(corr_matrix.shape), k=1).astype(bool)
            )
            
            strong_corrs = []
            for col in upper_triangle.columns:
                for idx in upper_triangle.index:
                    if upper_triangle.loc[idx, col] > threshold:
                        strong_corrs.append({
                            "pair": f"{idx} <-> {col}",
                            "correlation": upper_triangle.loc[idx, col]
                        })
            
            return {c["pair"]: c["correlation"] for c in sorted(
                strong_corrs,
                key=lambda x: x["correlation"],
                reverse=True
            )}
        
        return correlations.to_dict()
    
    def _build_dataframe_context(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Build context dictionary from DataFrame"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "sample": df.head(3).to_dict() if not df.empty else {},
            "stats": df.describe().to_dict() if not df.empty else {},
            "nulls": df.isnull().sum().to_dict(),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
    
    def suggest_analysis(self, df: pd.DataFrame) -> List[str]:
        """Suggest interesting analyses for a dataset"""
        suggestions_prompt = f"""
Given this dataset with columns: {', '.join(df.columns)}
Data types: {df.dtypes.to_dict()}

Suggest 5 interesting analysis questions that could be answered with this data.
Focus on actionable insights and business value.
"""
        
        response = self.think(
            prompt=suggestions_prompt,
            response_model=AgentResponse
        )
        
        return response.next_steps