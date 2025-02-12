import { Link } from "react-router-dom";
import "./HomePage.css";
import { Container, Row, Col, Card } from 'react-bootstrap';

export function HomePage() {
  return (
    <Container className="mt-5 pb-5">
      <Row>
        <h1 className="display-4 mb-4">Strava API Integration</h1>
        <Col md={4}>
          <Card className="text-center shadow">
            <Card.Body>
              <Card.Title>Your Strava API</Card.Title>
              <Card.Text>Pull all your Strava details into one place</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}