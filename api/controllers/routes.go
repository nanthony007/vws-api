package controllers

func (s *Server) initializeRoutes() {
	s.Router.GET("/", s.Home)
	s.Router.GET("/wrestlers", s.GetWrestlers)
}
