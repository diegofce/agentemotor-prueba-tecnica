import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  message: string | null;
}

export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { message: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { message: error.message };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("Error de interfaz:", error, info.componentStack);
  }

  render() {
    if (this.state.message !== null) {
      return (
        <main className="app">
          <h1 className="page-title">Cartera de pólizas</h1>
          <p className="inline-error section-error" role="alert">
            Error al renderizar la interfaz: {this.state.message}
          </p>
        </main>
      );
    }

    return this.props.children;
  }
}
